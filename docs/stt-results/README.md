# 📊 ChefEar STT 평가 결과

ChefEar STT 모델의 실험 및 최종 평가 결과를 정리한 폴더입니다.

## 📁 파일 안내

- `result.ipynb`: 전체 모델 실험 및 최종 선정 과정
- `ChefEar_STT_3model_comparison_final.csv`: 모델별 비교 결과
- `final_evaluation_summary.csv`: 최종 평가 요약
- `fixed100_predictions.csv`: Fixed100 문장별 예측 결과
- `new500_predictions.csv`: 신규500 문장별 예측 결과

## 🧪 평가 기준

- Fixed100 고정 문장 평가
- 신규500 일반화 성능 평가
- 숫자·수량·단위 인식 평가
- 재료명 및 조리동작 인식 평가
- TTS 음성 재인식 평가

## 📈 최종 결과

| 평가 지표 | 결과 |
|---|---:|
| Fixed100 WER | 7.68% |
| Fixed100 CER | 1.44% |
| 신규500 WER | 10.72% |
| 신규500 CER | 2.26% |
| 숫자·단위 인식 성공률 | 90.57% |
| 재료명 인식 성공률 | 98.31% |
| 조리동작 인식 성공률 | 99.54% |
| 핵심정보 종합 성공률 | 96.23% |

상세한 실험 과정은 [`result.ipynb`](./result.ipynb)에서 확인할 수 있습니다.

모델 가중치, 비공개 데이터, 음성 원본 및 인증 정보는 공개하지 않습니다.