# AGENTS.md

## 저장소 목적

ChefEar 팀 프로젝트에서 개인적으로 담당한 STT 모델 개발과 실험 결과를 정리한 저장소입니다.

주요 범위:

- Whisper 모델 비교 및 파인튜닝
- 요리 도메인 음성 데이터 처리
- WER·CER 평가와 오류 분석
- CTranslate2 변환
- faster-whisper 추론 검증
- STT 통합 테스트 문서화

TTS 모델 개발과 전체 서비스 오케스트레이션은 이 저장소의 범위가 아닙니다.

## 기술 구성

`Python` `PyTorch` `Transformers` `PEFT` `QLoRA` `Whisper` `wav2vec2` `CTranslate2` `faster-whisper` `jiwer` `CUDA`

최종 추론 흐름:

```text
QLoRA 파인튜닝
→ Adapter 병합
→ CTranslate2 변환
→ int8 경량화
→ faster-whisper 추론
```

## 저장소 구조

```text
chefear-stt/
├── AGENTS.md
├── README.md
├── stt/
├── docs/stt-results/
└── integration/
```

| 파일 및 폴더 | 역할 |
|---|---|
| `stt/infer.py` | STT 모델 로드 및 추론 |
| `stt/export_ct2.py` | CTranslate2 변환 |
| `stt/compare_realtime_models.py` | 추론 모델 비교 |
| `stt/requirements-stt.txt` | STT 의존성 |
| `docs/stt-results/` | 평가 결과 |
| `integration/` | 통합 테스트 자료 |

## 작업 규칙

- 요청한 파일과 관련된 범위만 수정합니다.
- 기존 변수명과 파일 구조를 유지합니다.
- 관련 없는 코드와 문서를 수정하지 않습니다.
- 불필요한 리팩터링을 하지 않습니다.
- 새로운 라이브러리와 설정을 임의로 추가하지 않습니다.
- TTS와 전체 팀 서비스 기능을 임의로 추가하지 않습니다.
- 확인하지 않은 성능 수치와 실행 결과를 작성하지 않습니다.
- 기존 사용자의 변경사항을 덮어쓰지 않습니다.

## 실행 및 검증

파인튜닝, 모델 변환 및 실시간 추론은 GPU 환경을 기준으로 합니다.

GPU 또는 비공개 모델이 없는 경우 다음 항목만 제한적으로 확인합니다.

- Python 문법
- import 구조
- 경로와 환경변수
- 함수 호출 구조
- 문서와 코드의 일치 여부

실제로 실행하지 못한 모델 추론과 평가를 완료된 것으로 보고하지 않습니다.

## 보안

다음 자료는 저장소에 추가하지 않습니다.

- 모델 가중치와 체크포인트
- QLoRA Adapter
- CTranslate2 변환 모델
- 비공개 음성 및 학습 데이터
- 토큰, API 키, 비밀번호
- `.env` 파일

## Git 규칙

- 작업은 별도 브랜치에서 진행합니다.
- `main` 브랜치에 직접 작업하지 않습니다.
- 작업 전후 `git status`를 확인합니다.
- commit, push, PR, merge는 사용자 승인 후 수행합니다.
- 강제 push와 기존 커밋 삭제를 하지 않습니다.
- 다른 사람의 작업으로 보이는 변경사항은 임의로 수정하지 않습니다.

## 완료 보고

작업 완료 후 다음 내용을 한국어로 보고합니다.

- 수정한 파일
- 변경 내용
- 검증 방법과 결과
- 실행하지 못한 항목
- 남은 문제
- 다음 단계
