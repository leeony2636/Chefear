# 🍳 ChefEar

AI 음성 레시피 어시스턴트 프로젝트에서 수행한 개인 STT 모델 개발 및 실험 결과를 정리한 저장소입니다.

요리 중 화면이나 키보드를 조작하기 어려운 상황에서도 음성으로 레시피를 조회하고 조리 단계를 진행할 수 있도록, 요리 도메인에 특화된 STT 모델을 개발했습니다.

## 🧑‍💻 담당 업무

- Whisper Small, wav2vec2, Whisper Large-v3-turbo 모델 비교
- Whisper Large-v3-turbo 기반 QLoRA 파인튜닝
- 요리 도메인 음성 데이터 전처리 및 학습
- Fixed100 / New500 데이터셋 기반 WER·CER 평가
- 최종 STT 모델 선정
- 숫자·수량·단위 표현 인식 보정
- TTS 음성 → STT 재인식 통합 테스트
- 파인튜닝 모델의 CTranslate2 변환 및 int8 경량화
- Git Branch / Pull Request / Review 기반 협업

## 🔊 STT 처리 흐름

> Voice Input  
> → Fine-tuned Whisper STT  
> → Recognized Text  
> → WER·CER Evaluation  
> → Voice Command Processing

## 🧠 모델 개발

Whisper Small, wav2vec2, Whisper Large-v3-turbo를 비교한 뒤, 요리 관련 음성 인식 성능과 확장성을 고려하여 Whisper Large-v3-turbo를 최종 기반 모델로 선정했습니다.

이후 요리명, 재료명, 수량, 단위, 조리 명령어가 포함된 데이터로 QLoRA 파인튜닝을 수행했습니다.

최종적으로 다음 Adapter를 기준 모델로 선정했습니다.

```text
BEST_FINAL_mix750_replay_numeric
```

V2 추가 파인튜닝도 진행했지만 성능 개선이 충분하지 않아, 현재 최종 모델은 V1 기반 Adapter를 사용합니다.

## 📊 평가

다음 데이터셋을 기준으로 모델 성능을 평가했습니다.

- Fixed100
- New500
- 고위험 음성 명령어 데이터
- 숫자·수량·단위 테스트 데이터
- TTS 출력 음성 재인식 데이터

주요 평가 지표는 다음과 같습니다.

- WER
- CER
- 요리명 인식 정확도
- 재료명 인식 정확도
- 수량 및 단위 인식 정확도
- 음성 명령어 인식 정확도

세부 평가 결과는 다음 폴더에서 확인할 수 있습니다.

```text
docs/stt-results/
docs/stt-comparison/
```

## ⚡ STT 모델 경량화

학습 및 오프라인 평가에서는 Transformers와 PEFT 기반의 QLoRA Adapter를 사용합니다.

실시간 추론과 배포를 위해서는 파인튜닝 모델을 CTranslate2 형식으로 변환하고 int8로 경량화합니다.

```text
Fine-tuned LoRA Adapter
→ Base Model과 병합
→ CTranslate2 변환
→ int8 양자화
→ faster-whisper 추론
```

배포용 모델은 다음과 같이 로드합니다.

```python
WhisperModel(
    model_path,
    device="cuda",
    compute_type="int8"
)
```

학습용 모델과 배포용 모델은 다음과 같이 구분됩니다.

| 구분 | 사용 방식 |
|---|---|
| 학습·오프라인 평가 | Transformers + PEFT + QLoRA |
| 실시간·배포 추론 | faster-whisper + CTranslate2 int8 |
| 기반 모델 | Whisper Large-v3-turbo |
| 최종 Adapter | `BEST_FINAL_mix750_replay_numeric` |

## 📁 폴더 안내

- `stt/`: STT 학습·추론·평가·변환 코드
- `docs/stt-results/`: WER·CER 및 최종 평가 결과
- `docs/stt-comparison/`: 모델 비교 및 실험 자료
- `integration/`: STT·TTS 재인식 및 통합 테스트 자료
- `tts/`: TTS 관련 테스트 참고 자료
- `orchestration/`: 실행 환경 및 모델 로딩 보조 코드

## 🧩 주요 코드

### 학습 및 평가용

```text
load_stt_model()
stt_transcribe_with_context()
run_batch_test()
```

QLoRA Adapter를 Transformers 기반으로 불러와 오프라인 평가와 모델 비교에 사용합니다.

### 배포 및 실시간 추론용

```text
load_ct2_model()
stt_transcribe()
```

CTranslate2 int8 모델을 faster-whisper로 로드하여 실시간 음성 인식에 사용합니다.

## 🔤 음성 인식 후처리

STT 결과에서 자주 사용되는 단위 표현을 한글 단위로 변환하는 후처리를 적용했습니다.

```text
g   → 그램
kg  → 킬로그램
ml  → 밀리리터
L   → 리터
```

또한 요리 음성에 자주 나타나는 숫자, 수량, 재료 표현을 보정하여 조리 명령어 인식의 안정성을 높였습니다.

## ⚙️ 실행 환경

- Python
- PyTorch
- Transformers
- PEFT
- bitsandbytes
- QLoRA
- Whisper Large-v3-turbo
- faster-whisper
- CTranslate2
- CUDA GPU

환경변수는 `.env.example`을 참고하여 로컬 `.env`에 설정합니다.

## 🔒 모델 보호

- 모델 가중치와 체크포인트는 저장소에 포함하지 않습니다.
- 파인튜닝 Adapter는 비공개 Hugging Face 저장소에서 관리합니다.
- 배포용 CTranslate2 모델도 저장소에 직접 포함하지 않습니다.
- 토큰, API 키, 비밀번호, `.env` 파일은 공개하지 않습니다.
- 학습 데이터와 원본 오디오는 저장소에 포함하지 않습니다.

## 🧪 통합 테스트

TTS가 생성한 음성을 다시 STT 모델에 입력하여 음성 인식 결과를 확인했습니다.

```text
TTS 음성 생성
→ STT 재인식
→ 원문과 결과 비교
→ CER·WER 측정
```

이를 통해 단순한 텍스트 입력 평가뿐 아니라 실제 음성 출력 환경에서의 인식 품질도 확인했습니다.

## 📌 최종 정리

이 프로젝트에서는 Whisper Large-v3-turbo를 기반으로 요리 도메인 음성 데이터에 QLoRA 파인튜닝을 적용했습니다.

모델 비교와 WER·CER 평가를 통해 최종 Adapter를 선정했으며, 실시간 서비스 적용을 위해 CTranslate2 int8 및 faster-whisper 기반의 추론 구조까지 구성했습니다.

이 저장소는 개인 STT 모델 개발, 파인튜닝, 평가, 경량화 및 통합 테스트 과정을 기록한 포트폴리오용 저장소입니다.
