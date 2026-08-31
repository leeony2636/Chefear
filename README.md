# 🍳 ChefEar STT

ChefEar 음성 레시피 어시스턴트 프로젝트에서 담당한 개인 STT 모델 개발 및 실험 결과를 정리한 저장소입니다.

ChefEar는 요리 중 손에 물이나 재료가 묻어 화면이나 키보드를 조작하기 어려운 상황에서도, 음성으로 레시피를 조회하고 조리 단계를 진행할 수 있도록 설계된 음성 레시피 서비스입니다.

본 저장소에서는 ChefEar 프로젝트에서 수행한 STT 모델 개발, 요리 도메인 파인튜닝, 성능 평가 및 실시간 추론 적용 과정을 중심으로 다룹니다.

## 🎯 STT 개발 목표

요리 중 사용자의 음성을 통해 다음 정보를 인식하는 것을 목표로 했습니다.

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

STT가 음성을 텍스트로 변환하면, 변환된 텍스트는 레시피 조회와 음성 명령 처리에 활용됩니다.

## 🧩 프로젝트 구성

| 구성 요소 | 역할 |
|---|---|
| STT | 사용자의 음성을 텍스트로 변환 |
| 의도 분석 | 레시피 조회 및 조리 명령 구분 |
| 레시피 처리 | 요리명과 조리 단계 검색 |
| TTS | 조리 단계와 안내 문장을 음성으로 출력 |

TTS는 팀 프로젝트의 별도 담당 영역이며, 본 저장소에서는 TTS 모델의 상세 개발·학습·평가를 다루지 않습니다.

## 🧑‍💻 담당 업무

본인이 담당한 핵심 영역은 STT 모델 개발입니다.

- Whisper Small, wav2vec2, Whisper Large-v3-turbo 모델 비교
- Whisper Large-v3-turbo 기반 QLoRA 파인튜닝
- 요리 도메인 음성 데이터 전처리 및 학습
- Fixed100·신규500 데이터셋 기반 평가
- WER·CER 기반 성능 비교
- 숫자·수량·단위 취약유형 분석
- 재료명·조리동작·긴 문장 인식 성능 분석
- 최종 STT 모델 선정
- TTS 음성의 STT 재인식 테스트
- CTranslate2 및 faster-whisper 기반 추론 경량화
- Git Branch / Pull Request / Review 기반 협업

STT 개발 과정과 모델 선정 근거는 [STT 개발 문서](./stt/README.md)에서 확인할 수 있습니다.

## 📊 STT 평가

STT 모델은 다음 기준으로 평가했습니다.

- Fixed100 고정 문장 평가
- 신규500 일반화 성능 평가
- 숫자·수량·단위 인식 평가
- 재료명 인식 평가
- 조리동작 인식 평가
- 긴 문장 처리 성능 분석
- TTS 음성 재인식 테스트

상세한 평가 결과와 문장별 예측 자료는 [STT 평가 결과](./docs/stt-results/README.md)에서 확인할 수 있습니다.

## 📁 폴더 안내

| 폴더 | 설명 |
|---|---|
| [`stt/`](./stt/) | STT 학습·추론·평가·변환 코드 |
| [`docs/stt-results/`](./docs/stt-results/) | STT 평가 결과 및 분석 자료 |
| [`integration/`](./integration/) | 팀 프로젝트에 STT를 적용한 통합 테스트 참고 자료 |

> 본 저장소의 핵심 개발 범위는 STT입니다. TTS 모델 개발은 팀원의 담당 영역이므로 이 저장소에는 포함하지 않습니다.

## ⚙️ 실행 환경

- Python
- PyTorch
- Transformers
- PEFT
- QLoRA
- Whisper Large-v3-turbo
- faster-whisper
- CTranslate2
- CUDA GPU

세부 실행 방법과 환경변수 설정은 [`stt/README.md`](./stt/README.md)와 `.env.example`을 참고합니다.

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

## 📌 프로젝트 정리

ChefEar는 음성 인식과 음성 합성 기술을 활용하여 요리 중 손을 사용하기 어려운 문제를 해결하는 것을 목표로 합니다.

본 저장소는 그중 개인적으로 담당한 STT 영역을 중심으로 구성되어 있습니다. STT 모델 개발, 요리 도메인 파인튜닝, 성능 평가, 오류 분석 및 실시간 추론 적용 과정을 포트폴리오 형태로 정리했습니다.
