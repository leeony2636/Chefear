# ChefEar STT

ChefEar 팀 프로젝트에서 개인적으로 담당한
STT 모델 개발 및 실험 결과를 정리한 저장소입니다.

ChefEar는 STT·의도 분석·레시피 처리·TTS가 결합된 팀 프로젝트이며,
본 저장소에서는 그중 개인적으로 담당한 STT 개발 과정만 다룹니다.

## 📌 저장소 범위

다음 내용을 중심으로 정리합니다.

- STT 모델 비교 및 선정
- Whisper 기반 요리 도메인 파인튜닝
- 음성 데이터 전처리
- WER·CER 기반 성능 평가
- 오류 유형 분석
- CTranslate2 변환
- faster-whisper 기반 추론 검증
- 팀 서비스 통합 테스트

TTS 모델 개발과 전체 서비스 오케스트레이션은 팀 프로젝트의
별도 담당 영역이며 본 저장소에는 포함하지 않습니다.

## 🎯 STT 개발 목표

요리 중 화면이나 키보드를 조작하기 어려운 상황에서도
음성으로 다음 정보를 인식하는 것을 목표로 했습니다.

- 요리명
- 재료명
- 수량
- 계량 단위
- 조리동작
- 조리 단계 진행 명령
- 긴 조리 안내 문장

## 🔊 STT 처리 흐름

```text
Voice Input
→ Fine-tuned Whisper STT
→ Recognized Text
→ Recipe / Voice Command Processing
```

STT 모델이 변환한 텍스트는 ChefEar 서비스의
레시피 조회와 조리 명령 처리에 활용됩니다.

## 🧑‍💻 담당 업무

- Whisper Small, wav2vec2, Whisper Large-v3-turbo 비교
- Whisper Large-v3-turbo 기반 QLoRA 파인튜닝
- 요리 도메인 음성 데이터 전처리 및 학습
- Fixed100·신규500 데이터셋 기반 평가
- WER·CER 기반 성능 비교
- 숫자·수량·단위 취약유형 분석
- 재료명·조리동작·긴 문장 인식 분석
- 최종 STT 모델 선정
- TTS 출력 음성의 STT 재인식 테스트
- CTranslate2 int8 변환 및 추론 구조 검증
- Git Branch·Pull Request·Review 기반 협업

## 🧠 모델 구성

Whisper Small, wav2vec2, Whisper Large-v3-turbo를 비교한 결과,
한국어 음성 인식 성능과 요리 도메인 적용 가능성을 고려하여
Whisper Large-v3-turbo를 기반 모델로 선정했습니다.

이후 요리명, 재료명, 숫자, 단위, 조리동작 및 음성 명령이 포함된
데이터에 QLoRA 파인튜닝을 적용했습니다.

평가 과정에서 확인된 오류 유형을 분석하고,
숫자·수량·단위와 같은 취약유형 데이터를 보강했습니다.

## 🧪 평가 방법

### Fixed100

고정된 100개 문장을 사용하여 기본 음성 인식 성능을 평가했습니다.

### 신규500

학습에 사용하지 않은 신규 500개 문장을 사용하여
새로운 문장에 대한 일반화 성능을 평가했습니다.

### 도메인 핵심정보 평가

요리 서비스에서 중요한 다음 항목을 별도로 평가했습니다.

- 숫자·수량·단위
- 재료명
- 조리동작
- 긴 문장
- 발음이 유사한 표현

### TTS 음성 재인식 테스트

TTS가 생성한 음성을 STT 모델에 다시 입력하여
실제 음성 출력 환경에서의 인식 결과를 확인했습니다.

```text
TTS 음성 생성
→ STT 재인식
→ 정답 문장 비교
→ WER·CER 측정
```

TTS 모델 자체의 개발과 학습은 본인의 담당 범위가 아니며,
본 저장소에서는 TTS 출력 음성을 활용한 STT 재인식 테스트만 다룹니다.

## 📊 최종 평가 결과

| 평가 지표 | 결과 |
|---|---:|
| Fixed100 WER | 7.68% |
| Fixed100 CER | 1.44% |
| 신규500 WER | 10.72% |
| 신규500 CER | 2.26% |
| 문장 전체 일치율 | 61.80% |
| 숫자·단위 인식 성공률 | 90.57% |
| 재료명 인식 성공률 | 98.31% |
| 조리동작 인식 성공률 | 99.54% |
| 핵심정보 종합 성공률 | 96.23% |

최종 모델은 WER·CER 하나만으로 결정하지 않고,
신규 문장에 대한 일반화 성능과 요리 도메인 핵심정보 인식 결과를
종합하여 선정했습니다.

상세한 평가 결과는
[STT 평가 결과](./docs/stt-results/README.md)에서 확인할 수 있습니다.

## ⚡ 모델 경량화 및 적용

학습용 모델과 실시간 추론용 모델을 구분하여 관리했습니다.

```text
QLoRA 파인튜닝 모델
→ Base Model과 Adapter 병합
→ CTranslate2 형식 변환
→ int8 경량화
→ faster-whisper 기반 추론
```

CTranslate2 변환과 faster-whisper 기반 실시간 추론은
팀 GPU 환경에서 검증했습니다.

개인 PC에 CUDA GPU가 없거나 비공개 모델 접근 권한이 없는 경우에는
모델을 직접 실행하기 어렵지만, 코드 구조와 평가 결과는 확인할 수 있습니다.

## 📁 저장소 구조

```text
chefear-stt/
├── AGENTS.md
├── README.md
├── stt/
│   ├── infer.py
│   ├── export_ct2.py
│   ├── compare_realtime_models.py
│   ├── requirements-stt.txt
│   ├── README.md
│   └── stt.md
├── docs/
│   └── stt-results/
└── integration/
```

| 파일 및 폴더 | 설명 |
|---|---|
| [`AGENTS.md`](./AGENTS.md) | 저장소 작업 규칙 |
| [`stt/infer.py`](./stt/infer.py) | STT 모델 로드 및 추론 |
| [`stt/export_ct2.py`](./stt/export_ct2.py) | CTranslate2 변환 |
| [`stt/compare_realtime_models.py`](./stt/compare_realtime_models.py) | 실시간 추론 모델 비교 |
| [`stt/requirements-stt.txt`](./stt/requirements-stt.txt) | STT 관련 의존성 |
| [`stt/stt.md`](./stt/stt.md) | 학습 당시 환경 및 설정 |
| [`docs/stt-results/`](./docs/stt-results/) | 평가 수치와 예측 결과 |
| [`integration/`](./integration/) | 팀 서비스 통합 테스트 자료 |

## 🤝 팀 프로젝트 협업

ChefEar 팀 프로젝트에서는 다음과 같이 협업했습니다.

- STT 모델을 팀 서비스에 연결
- TTS 출력 음성의 STT 재인식 테스트
- 팀 GPU 환경에서 실시간 추론 구조 검증
- 팀원 코드와의 인터페이스 조율
- Git Branch·Pull Request·Review 기반 협업

본 저장소는 개인 STT 영역을 중심으로 관리하며,
ChefEar 전체 서비스 코드는 팀 프로젝트 저장소에서 관리합니다.

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
- jiwer
- CUDA GPU

파인튜닝 및 오프라인 평가는 GPU 환경에서 수행했습니다.

세부 환경 정보는
[stt/README.md](./stt/README.md)와
[stt/requirements-stt.txt](./stt/requirements-stt.txt)에서 확인할 수 있습니다.

## 🔒 모델 및 데이터 보호

다음 자료는 저장소에 포함하지 않습니다.

- 모델 가중치와 체크포인트
- QLoRA Adapter
- CTranslate2 변환 모델
- 비공개 음성 및 학습 데이터
- 비공개 모델 접근 정보
- 토큰, API 키, 비밀번호
- `.env` 파일

## 📚 관련 문서

- [STT 개발 문서](./stt/README.md)
- [STT 평가 결과](./docs/stt-results/README.md)
- [STT 통합 테스트 자료](./integration/README.md)

## 📌 정리

ChefEar 팀 프로젝트에서 개인적으로 STT 모델 개발을 담당했습니다.

Whisper Large-v3-turbo를 기반으로 요리 도메인 음성 데이터에
QLoRA 파인튜닝을 적용하고, Fixed100·신규500 평가를 통해
기본 성능과 일반화 성능을 확인했습니다.

또한 숫자·수량·단위와 같은 취약유형을 분석하고,
CTranslate2 int8 및 faster-whisper 기반 실시간 추론 구조를
팀 GPU 환경에서 검증했습니다.

본 저장소는 ChefEar 전체 프로젝트가 아닌,
개인적으로 수행한 STT 모델 개발·평가·오류 분석·경량화 및
팀 협업 과정을 정리한 포트폴리오입니다.
