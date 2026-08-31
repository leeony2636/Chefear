# 🍳 ChefEar STT

ChefEar 팀 프로젝트에서 개인적으로 담당한 STT 모델 개발과 실험 결과를 정리한 포트폴리오 저장소입니다.

ChefEar는 요리 중 손에 물이나 재료가 묻어 화면이나 키보드를 조작하기 어려운 상황에서도, 음성으로 레시피를 조회하고 조리 단계를 진행할 수 있도록 설계된 음성 레시피 서비스입니다.

본 저장소는 ChefEar 전체 서비스가 아닌, 그중 개인적으로 담당한 STT 모델 개발·평가·경량화 과정을 중심으로 구성되어 있습니다.

## 📌 저장소 범위

본인이 담당한 영역은 다음과 같습니다.

- Whisper 기반 STT 모델 비교
- 요리 도메인 음성 데이터 기반 QLoRA 파인튜닝
- STT 성능 평가 및 오류 분석
- 숫자·수량·단위 인식 성능 검토
- 최종 STT 모델 선정
- CTranslate2 int8 변환 과정 정리
- faster-whisper 기반 실시간 추론 검증
- ChefEar 팀 서비스와의 STT 통합 테스트

TTS 모델 개발과 학습은 팀 프로젝트의 별도 담당 영역입니다. 따라서 TTS 모델과 가중치는 본 저장소에 포함하지 않습니다.

## 🎯 STT 개발 목표

요리 중 사용자의 음성을 통해 다음 정보를 정확하게 인식하는 것을 목표로 했습니다.

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

STT 모델이 변환한 텍스트는 ChefEar 서비스의 레시피 조회와 조리 명령 처리에 활용됩니다.

## 🧩 ChefEar 프로젝트 내 역할

| 구성 요소 | 역할 |
|---|---|
| STT | 사용자의 음성을 텍스트로 변환 |
| 의도 분석 | 레시피 조회와 조리 명령 구분 |
| 레시피 처리 | 요리명과 조리 단계 검색 |
| TTS | 조리 단계와 안내 문장을 음성으로 출력 |

본 저장소에서는 STT 모델 개발을 중심으로 다룹니다. TTS 모델 자체의 개발·학습·평가는 팀 프로젝트의 다른 담당 영역에서 진행되었습니다.

## 🧑‍💻 STT 담당 업무

- Whisper Small, wav2vec2, Whisper Large-v3-turbo 비교
- Whisper Large-v3-turbo 기반 QLoRA 파인튜닝
- 요리 도메인 음성 데이터 전처리 및 학습
- Fixed100·신규500 데이터셋 기반 평가
- WER·CER 기반 성능 비교
- 숫자·수량·단위 취약유형 분석
- 재료명·조리동작·긴 문장 인식 분석
- 최종 STT 모델 선정
- TTS 출력 음성의 STT 재인식 테스트
- CTranslate2 int8 변환 과정 정리
- faster-whisper 기반 추론 구조 검증
- Git Branch·Pull Request·Review 기반 협업

## 🧠 기반 모델 및 파인튜닝

여러 STT 모델을 비교한 결과, 한국어 음성 인식 성능과 요리 도메인 적용 가능성을 고려하여 Whisper Large-v3-turbo를 기반 모델로 선정했습니다.

이후 요리명, 재료명, 숫자, 단위, 조리동작 및 음성 명령이 포함된 데이터에 QLoRA 파인튜닝을 적용했습니다.

평가 과정에서 확인된 오류 유형을 분석하고, 숫자·수량·단위와 같은 요리 도메인 취약유형 데이터를 보강했습니다.

## 🧪 평가 방법

### Fixed100

고정된 100개 문장을 사용하여 기본 음성 인식 성능을 평가했습니다.

### 신규500

학습에 사용하지 않은 신규 500개 문장을 사용하여 새로운 문장에 대한 일반화 성능을 평가했습니다.

### 도메인 핵심정보 평가

요리 서비스에서 중요한 다음 항목을 별도로 평가했습니다.

- 숫자·수량·단위
- 재료명
- 조리동작
- 긴 문장
- 발음이 유사한 표현

### TTS 음성 재인식 테스트

TTS가 생성한 음성을 STT 모델에 다시 입력하여 실제 음성 출력 환경에서의 인식 결과를 확인했습니다.

> TTS 모델 자체의 개발과 학습은 본인의 담당 범위가 아닙니다. 본 저장소에서는 TTS 출력 음성을 STT 평가에 활용한 재인식 테스트만 다룹니다.

```text
TTS 음성 생성
→ STT 재인식
→ 정답 문장 비교
→ WER·CER 측정
```

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

WER·CER뿐 아니라 요리 서비스에 필요한 핵심정보 인식 결과와 신규 문장에 대한 일반화 성능을 함께 고려하여 최종 모델을 선정했습니다.

상세한 결과는 [STT 평가 결과](./docs/stt-results/README.md)에서 확인할 수 있습니다.

## ⚡ 모델 경량화 및 적용

학습용 모델과 실시간 추론용 모델을 구분하여 관리했습니다.

```text
QLoRA 파인튜닝 모델
→ Base Model과 Adapter 병합
→ CTranslate2 형식 변환
→ int8 경량화
→ faster-whisper 기반 추론
```

CTranslate2 변환과 faster-whisper 기반 실시간 추론은 팀 GPU 환경에서 검증했습니다.

개인 PC에 CUDA GPU가 없는 경우에도 코드 구조와 평가 결과는 확인할 수 있지만, 실제 모델 추론에는 CUDA GPU와 비공개 모델 접근 권한이 필요합니다.

## 📁 폴더 안내

| 폴더 | 설명 |
|---|---|
| [`stt/`](./stt/) | STT 모델 로드·추론·평가·변환 코드 |
| [`docs/stt-results/`](./docs/stt-results/) | 모델 비교 및 STT 평가 결과 |
| [`integration/`](./integration/) | ChefEar 팀 서비스에 STT를 적용한 통합 테스트 참고 자료 |

## 🤝 팀 프로젝트 협업

개인적으로 STT 모델 개발과 평가를 담당했으며, ChefEar 팀 프로젝트에서는 다음과 같이 협업했습니다.

- STT 모델을 통합 서비스에 연결
- 음성 입력부터 레시피 처리까지의 통합 테스트
- TTS 출력 음성의 STT 재인식 테스트
- CTranslate2 int8 변환 모델의 팀 GPU 환경 검증
- 팀원 코드와의 인터페이스 조율
- Git Branch·Pull Request·Review 기반 협업

본 저장소는 개인 STT 영역을 중심으로 관리하며, ChefEar 전체 서비스 코드는 팀 프로젝트 저장소에서 관리합니다.

## ⚙️ 실행 및 검증 환경

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

파인튜닝 및 오프라인 평가는 GPU 환경에서 수행했습니다.

CTranslate2 변환과 faster-whisper 기반 실시간 추론은 팀 GPU 환경에서 검증했습니다.

세부 환경 정보는 [`stt/README.md`](./stt/README.md)와 [`stt/requirements-stt.txt`](./stt/requirements-stt.txt)에서 확인할 수 있습니다.

## 🔒 모델 및 데이터 보호

- 모델 가중치와 체크포인트는 저장소에 포함하지 않습니다.
- 파인튜닝 Adapter와 배포용 변환 모델은 공개하지 않습니다.
- 비공개 모델 저장소의 접근 정보는 공개하지 않습니다.
- 토큰, API 키, 비밀번호 및 `.env` 파일은 공개하지 않습니다.
- 학습 음성 및 비공개 학습 데이터는 저장소에 포함하지 않습니다.

## 📚 관련 문서

- [STT 개발 문서](./stt/README.md)
- [STT 평가 결과](./docs/stt-results/README.md)
- [STT 통합 테스트 자료](./integration/README.md)

## 📌 정리

ChefEar 팀 프로젝트에서 개인적으로 STT 모델 개발을 담당했습니다.

Whisper Large-v3-turbo를 기반으로 요리 도메인 음성 데이터에 QLoRA 파인튜닝을 적용하고, Fixed100·신규500 평가를 통해 기본 성능과 일반화 성능을 확인했습니다.

또한 숫자·수량·단위와 같은 취약유형을 분석하고, CTranslate2 int8 및 faster-whisper 기반 실시간 추론 구조를 팀 GPU 환경에서 검증했습니다.

본 저장소는 ChefEar 전체 프로젝트가 아닌, 개인적으로 수행한 STT 모델 개발·평가·오류 분석·경량화 및 팀 협업 과정을 정리한 포트폴리오입니다.
