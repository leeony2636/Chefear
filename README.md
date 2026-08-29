# ChefEar

AI 음성 레시피 어시스턴트 팀 프로젝트에서 수행한 개인 STT 작업 기록 저장소입니다.

## STT 작업 내용

- Whisper Small, wav2vec2, Whisper Large-v3-turbo 비교
- Whisper Large-v3-turbo 기반 QLoRA 파인튜닝
- WER/CER 기반 성능 평가
- TTS 음성 → STT 인식 통합 테스트
- 단독 추론용 `stt/infer.py` 및 서비스 호출 흐름 정리

## 폴더 안내

- `stt/`: STT 추론 코드, 모델 비교·변환 스크립트, 실행 의존성
- `docs/stt-results/`: 최종 평가 결과
- `docs/stt-comparison/`: 비교 실험 설정 및 결과 자료
- `integration/`: 팀 서비스 통합 참고 자료
- `tts/`: TTS 관련 참고 영역

## 모델 보호

모델 가중치는 저장소에 포함하지 않습니다. 실행 시 Hugging Face의 비공개 모델 저장소를 환경변수로 호출합니다.
토큰과 환경설정 파일은 저장소에 올리지 않습니다.

## 테스트

`stt/infer.py`는 파일 경로 또는 NumPy 파형을 입력으로 받아 STT 결과를 반환합니다. GPU 환경에서 Hugging Face Adapter 또는 CTranslate2 변환 모델을 호출해 단독 테스트할 수 있습니다.

팀 원본 저장소의 최신 코드는 별도 저장소에서 관리하며, 이 저장소는 개인 작업과 실험 결과를 기록하는 용도로 사용합니다.
