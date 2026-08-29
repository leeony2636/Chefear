# ChefEar

AI 음성 레시피 어시스턴트 팀 프로젝트에서 수행한 개인 STT 작업과 실험 결과를 정리한 저장소입니다.

요리 중 화면이나 키보드를 조작하기 어려운 상황에서도 음성으로 레시피를 조회하고 조리 단계를 진행할 수 있도록 STT·TTS·오케스트레이션 구조를 결합했습니다.

## 담당 업무

- Whisper Small, wav2vec2, Whisper Large-v3-turbo 비교
- Whisper Large-v3-turbo 기반 QLoRA 파인튜닝
- Fixed100 / New500 데이터셋 기준 WER·CER 평가
- 최종 STT 모델 선정
- TTS 음성 → STT 인식 통합 테스트
- Git Branch / Pull Request / Review 기반 협업

## STT 처리 흐름

```text
Voice Input
→ Fine-tuned Whisper STT
→ Intent / Recipe Processing
→ TTS
→ Voice Response

폴더 안내
- stt/: STT 추론·비교·변환 코드와 실행 정보
- docs/stt-results/: 최종 평가 결과
- docs/stt-comparison/: 모델 비교 및 실험 자료
- integration/: 서비스 통합 참고 자료
- tts/: TTS 관련 참고 자료
- orchestration/: 환경변수 로딩 등 실행 보조 코드
실행 환경
- Python
- PyTorch
- Transformers
- PEFT / QLoRA
- Whisper
- faster-whisper
- CUDA GPU 추론
환경변수는 .env.example을 참고해 로컬 .env에 설정합니다.
모델 보호
- 모델 가중치와 체크포인트는 저장소에 포함하지 않습니다.
- 실제 STT 모델은 비공개 Hugging Face 저장소에서 실행 시 호출합니다.
- 토큰, API 키, 비밀번호, .env 파일은 공개하지 않습니다.
- 학습 데이터와 원본 오디오도 저장소에 포함하지 않습니다.

 참고
팀 프로젝트의 최신 서비스 코드는 팀 저장소에서 관리하며, 이 저장소는 개인 STT 파인튜닝·평가·실험 과정을 기록하는 포트폴리오용 저장소입니다.
