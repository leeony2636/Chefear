# ChefEar

AI 음성 레시피 어시스턴트 팀 프로젝트에서 수행한 개인 STT 작업 기록 저장소입니다.

## STT 작업

- Whisper Small, wav2vec2, Whisper Large-v3-turbo 비교
- Whisper Large-v3-turbo 기반 QLoRA 파인튜닝
- WER/CER 성능 평가
- TTS 음성 → STT 통합 테스트
- 단독 추론용 `stt/infer.py` 정리

## 폴더 안내

- `stt/`: STT 추론·비교·변환 코드와 실행 정보
- `docs/stt-results/`: 최종 평가 결과
- `docs/stt-comparison/`: 모델 비교 자료
- `integration/`: 서비스 통합 참고 영역
- `tts/`: TTS 참고 영역

## 모델 보호

모델 가중치는 저장소에 포함하지 않습니다. 실행 시 Hugging Face 비공개 모델 저장소를 환경변수로 호출하며, 토큰과 `.env`는 업로드하지 않습니다.

팀 프로젝트의 최신 코드는 별도 저장소에서 관리하고, 이 저장소는 개인 작업과 실험 결과를 기록하는 용도로 사용합니다.
