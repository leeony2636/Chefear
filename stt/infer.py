"""ChefEar 개인 STT 모델 오프라인 평가 코드.

Whisper Large-v3-turbo Base Model에 비공개 QLoRA Adapter를 결합한 뒤
음성 파일을 일괄 추론하고 WER를 계산합니다.

이 파일은 QLoRA 4-bit NF4 기반 평가용 코드입니다.
CTranslate2 int8 변환과 faster-whisper 실시간 추론은 별도의 배포 환경에서 수행합니다.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import librosa
import pandas as pd
import torch
from dotenv import load_dotenv
from jiwer import wer
from peft import PeftModel
from transformers import (
    BitsAndBytesConfig,
    WhisperForConditionalGeneration,
    WhisperProcessor,
)


load_dotenv()

MODEL_ID = "openai/whisper-large-v3-turbo"
HF_ADAPTER_ID = os.getenv("HF_STT_MODEL_REPO")
HF_TOKEN = os.getenv("HF_TOKEN") or None

_processor: Optional[WhisperProcessor] = None
_model = None
_input_dtype: Optional[torch.dtype] = None


def _get_adapter_id() -> str:
    """비공개 QLoRA Adapter 저장소 설정을 확인합니다."""
    if not HF_ADAPTER_ID:
        raise RuntimeError(
            "HF_STT_MODEL_REPO가 설정되지 않았습니다. "
            ".env에 비공개 Adapter 저장소를 설정하세요."
        )
    return HF_ADAPTER_ID


def get_input_dtype(model) -> torch.dtype:
    """Whisper encoder 입력에 사용할 dtype을 확인합니다."""
    for name, module in model.named_modules():
        if name.endswith("encoder.conv1") and getattr(module, "bias", None) is not None:
            return module.bias.dtype
    return torch.float16


def load_stt_model():
    """Whisper Base Model과 ChefEar QLoRA Adapter를 한 번만 로드합니다.

    QLoRA 4-bit NF4 모델은 CUDA GPU 환경에서 실행해야 합니다.
    """
    global _processor, _model, _input_dtype

    if _model is not None and _processor is not None:
        return _model, _processor

    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA GPU가 필요합니다. 이 코드는 QLoRA 4-bit NF4 평가용입니다."
        )

    adapter_id = _get_adapter_id()

    try:
        _processor = WhisperProcessor.from_pretrained(adapter_id, token=HF_TOKEN)
    except Exception:
        _processor = WhisperProcessor.from_pretrained(MODEL_ID, token=HF_TOKEN)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    base_model = WhisperForConditionalGeneration.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        token=HF_TOKEN,
    )
    base_model.config.forced_decoder_ids = None
    base_model.generation_config.forced_decoder_ids = None

    _model = PeftModel.from_pretrained(base_model, adapter_id, token=HF_TOKEN)
    _model.eval()
    _model.config.forced_decoder_ids = None
    _model.generation_config.forced_decoder_ids = None
    _input_dtype = get_input_dtype(_model)

    print("ChefEar STT QLoRA 모델 로드 완료")
    print(f"Base Model: {MODEL_ID}")
    print(f"Input dtype: {_input_dtype}")
    return _model, _processor


def transcribe_audio(audio_path: str | Path) -> str:
    """음성 파일 하나를 16kHz mono로 변환하여 인식합니다."""
    model, processor = load_stt_model()
    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {audio_path}")

    audio, _ = librosa.load(str(audio_path), sr=16000, mono=True)
    inputs = processor(
        audio,
        sampling_rate=16000,
        return_tensors="pt",
        return_attention_mask=True,
    )

    device = next(model.parameters()).device
    input_dtype = _input_dtype or get_input_dtype(model)
    input_features = inputs.input_features.to(device=device, dtype=input_dtype)
    attention_mask = inputs.attention_mask.to(device)

    with torch.no_grad():
        generated_ids = model.generate(
            input_features=input_features,
            attention_mask=attention_mask,
            language="ko",
            task="transcribe",
        )

    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()


def _find_audio_file(audio_dir: Path, test_id: str) -> Path | None:
    """test_id에 대응하는 음성 파일을 찾습니다."""
    for extension in (".mp3", ".wav", ".m4a", ".flac"):
        path = audio_dir / f"{test_id}{extension}"
        if path.exists():
            return path
    return None


def run_batch_test(
    csv_path: str | Path,
    audio_dir: str | Path,
    result_path: str | Path = "ChefEar_STT_test_result.csv",
) -> pd.DataFrame:
    """CSV 정답 문장과 음성 파일을 비교하여 WER 결과를 저장합니다.

    CSV에는 ``test_id``와 ``text`` 컬럼이 필요합니다.
    """
    csv_path = Path(csv_path)
    audio_dir = Path(audio_dir)
    result_path = Path(result_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
    if not audio_dir.exists():
        raise FileNotFoundError(f"오디오 폴더를 찾을 수 없습니다: {audio_dir}")

    df = pd.read_csv(csv_path)
    required_columns = {"test_id", "text"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"CSV에 필요한 컬럼이 없습니다: {sorted(missing_columns)}")

    load_stt_model()
    results = []

    for _, row in df.iterrows():
        test_id = str(row["test_id"])
        reference = str(row["text"])
        audio_path = _find_audio_file(audio_dir, test_id)

        if audio_path is None:
            results.append({
                "test_id": test_id,
                "audio_file": "",
                "reference": reference,
                "prediction": "",
                "wer": None,
                "status": "audio_not_found",
            })
            continue

        try:
            prediction = transcribe_audio(audio_path)
            score = wer(reference, prediction)
            status = "success"
        except Exception as exc:
            prediction = ""
            score = None
            status = f"error: {type(exc).__name__}"

        results.append({
            "test_id": test_id,
            "audio_file": audio_path.name,
            "reference": reference,
            "prediction": prediction,
            "wer": score,
            "status": status,
        })

    result_df = pd.DataFrame(results)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(result_path, index=False, encoding="utf-8-sig")
    print(f"평가 결과 저장 완료: {result_path}")
    return result_df


if __name__ == "__main__":
    print(
        "함수 호출용 평가 모듈입니다. "
        "run_batch_test(csv_path, audio_dir, result_path)를 사용하세요."
    )
