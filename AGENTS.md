# AGENTS.md

이 저장소는 ChefEar 팀 프로젝트에서 개인적으로 담당한
STT 모델 개발과 실험 결과를 정리한 포트폴리오 저장소입니다.

## 1. 저장소의 목적

이 저장소에서는 다음 작업을 다룹니다.

- STT 모델 비교
- Whisper 기반 요리 도메인 파인튜닝
- 음성 데이터 전처리
- WER·CER 성능 평가
- STT 오류 유형 분석
- CTranslate2 변환
- faster-whisper 기반 추론 검증
- STT 통합 테스트 문서화

TTS 모델 자체의 개발·학습·평가와 전체 서비스 오케스트레이션은
이 저장소의 직접적인 개발 범위가 아닙니다.

TTS는 STT 재인식 테스트에 필요한 경우에만 참고합니다.

## 2. 모델 구성

비교한 모델은 다음과 같습니다.

- Whisper Small
- wav2vec2
- Whisper Large-v3-turbo

최종 STT 모델은 Whisper Large-v3-turbo를 기반으로
QLoRA 파인튜닝을 적용한 모델입니다.

실시간 추론 적용 과정에서는 다음 흐름을 사용합니다.

```text
파인튜닝 모델
→ Base Model과 Adapter 병합
→ CTranslate2 형식 변환
→ int8 경량화
→ faster-whisper 추론

3. 저장소 구조

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
│       ├── README.md
│       ├── result.ipynb
│       ├── fixed100_predictions.csv
│       ├── new500_predictions.csv
│       ├── final_evaluation_summary.csv
│       └── ChefEar_STT_3model_comparison_final.csv
└── integration/
    └── README.md

    파일을 수정하기 전에는 해당 파일의 역할과 연결된 실행 흐름을 확인합니다.
4. 파일별 역할
- stt/infer.py: STT 모델 로드 및 음성 인식
- stt/export_ct2.py: CTranslate2 변환 과정
- stt/compare_realtime_models.py: 실시간 추론 모델 비교
- stt/requirements-stt.txt: STT 관련 의존성
- stt/stt.md: 학습 당시 환경 및 설정 기록
- docs/stt-results/: 평가 수치와 예측 결과
- integration/: 팀 서비스 통합 테스트 참고 자료
5. 평가 기준
STT 모델은 단일 지표만으로 판단하지 않습니다.
다음 항목을 함께 확인합니다.
- Fixed100 성능
- New500 일반화 성능
- WER
- CER
- 문장 전체 일치율
- 요리명 인식
- 재료명 인식
- 숫자·수량·계량 단위 인식
- 조리동작 인식
- 긴 문장 처리
- 발음이 유사한 표현 처리
- TTS 출력 음성 재인식 결과
평가 수치와 데이터셋 이름은 실제 문서와 결과 파일을 확인한 뒤 사용합니다.
확인되지 않은 수치나 결과를 새로 작성하지 않습니다.
6. 실행 환경
파인튜닝, 모델 변환 및 실시간 추론은 GPU 환경을 기준으로 합니다.
개인 PC에 CUDA GPU가 없거나 비공개 모델에 접근할 수 없는 경우에는
다음 항목만 제한적으로 확인할 수 있습니다.
- Python 문법
- import 구조
- 파일 경로 처리
- 환경변수 처리
- 함수 호출 구조
- 문서와 코드의 일치 여부
실제로 실행하지 못한 모델 추론이나 평가를 완료된 것으로 보고하지 않습니다.
7. 모델 및 데이터 보호
다음 자료는 저장소에 추가하지 않습니다.
- 모델 가중치
- 체크포인트
- QLoRA Adapter
- CTranslate2 변환 모델
- 비공개 음성 데이터
- 학습 원본 데이터
- Hugging Face 토큰
- API 키
- 비밀번호
- .env 파일
필요한 모델과 데이터는 환경변수 또는 사용자가 직접 지정하는 경로를 사용합니다.
8. 작업 원칙
- 요청한 파일과 관련된 범위만 수정합니다.
- 기존 파일 구조와 변수명을 임의로 변경하지 않습니다.
- 관련 없는 코드와 문서를 수정하지 않습니다.
- 새로운 라이브러리와 설정을 임의로 추가하지 않습니다.
- 불필요한 리팩터링을 하지 않습니다.
- 모델 성능이나 실행 결과를 추측하지 않습니다.
- 기존 사용자의 변경사항을 덮어쓰지 않습니다.
- TTS와 전체 팀 서비스 기능을 이 저장소에 임의로 추가하지 않습니다.
9. 오류 처리
오류가 발생하면 다음 순서로 보고합니다.
1. 오류가 발생한 위치
2. 확인된 원인
3. 가장 작은 수정 방법
4. 수정 내용
5. 검증 결과
6. 남아 있는 제한사항
근거 없이 여러 파일을 동시에 수정하지 않습니다.
10. Git 작업 규칙
- 작업은 별도 작업 브랜치에서 진행합니다.
- main 브랜치에 직접 작업하지 않습니다.
- 작업 전 git status를 확인합니다.
- 작업 후 변경 파일을 확인합니다.
- commit, push, pull request, merge는 사용자의 승인을 받은 후 수행합니다.
- 강제 push와 기존 커밋 삭제를 수행하지 않습니다.
- 다른 사람의 작업으로 보이는 변경사항은 임의로 수정하지 않습니다.
11. 완료 보고
작업이 끝나면 한국어로 다음 내용을 보고합니다.
- 수정한 파일
- 주요 변경 내용
- 수행한 검증
- 검증 결과
- 실행하지 못한 항목
- 남아 있는 문제
- 다음 단계
검증하지 못한 항목은 반드시 그 이유를 함께 기록합니다.