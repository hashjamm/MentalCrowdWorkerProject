# API 가이드: 전체 설문 종합 평가

---

## 1. Endpoint

```
POST /MentalCrowdWorkerProjectApp/app_calculate_whole_scores/
```

## 2. 설명

요청 본문에 포함된 모든 설문(PSQI, WHODAS, DASS-21, LSIS) 데이터를 종합하여, 각 설문의 평가 결과를 하나의 JSON 객체로 병합하여 반환합니다. 이 API는 데이터를 저장하지 않고 계산 결과만 반환합니다.

## 3. 파라미터 (Parameters)

- 없음

## 4. 요청 본문 (Request Body)

요청 본문에는 각 설문 데이터가 중첩된 JSON 객체 형태로 포함되어야 합니다.

### 4.1. 요청 예시 (Example)

```json
{
    "PSQI_data": {
        "result_1": "23:00:00",
        "result_2": 30,
        // ... PSQI 모든 필드
    },
    "WHODAS_data": {
        "result_1": 1,
        "result_2": 2,
        // ... WHODAS 모든 필드
    },
    "DASS21_data": {
        "result_1": 1,
        "result_2": 2,
        // ... DASS-21 모든 필드
    },
    "LSIS_data": {
        "result_1": 2,
        "result_2": 3,
        // ... LSIS 모든 필드
    }
}
```

### 4.2. 데이터 모델 (WholeScores Request Schema)

| 필드 (Field) | 타입 (Type) | 설명 (Description) |
| :--- | :--- | :--- |
| `PSQI_data` | `object` | 수면 건강(PSQI) 설문 데이터 객체. 상세 스키마는 `calculate_psqi.md` 참고. |
| `WHODAS_data` | `object` | 일반 건강(WHODAS) 설문 데이터 객체. 상세 스키마는 `calculate_whodas.md` 참고. |
| `DASS21_data` | `object` | 감정 상태(DASS-21) 설문 데이터 객체. 상세 스키마는 `calculate_dass21.md` 참고. |
| `LSIS_data` | `object` | 외로움(LSIS) 설문 데이터 객체. 상세 스키마는 `calculate_lsis.md` 참고. |

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

모든 설문의 계산된 점수와 상태가 하나의 JSON 객체로 통합되어 반환됩니다.

```json
{
    "sleep_quality_score": 0,
    "psqi_k_status": "숙면을 취하고 있는 상태",
    "cognition_score": 2,
    "whodas_k_status": "건강기능에 주의가 필요한 상태",
    "depression_score": 14,
    "dass_status": "매우 심각한 상태",
    "loneliness_score": 4,
    "lsis_status": "사회적 관계 단절과 외로움이 우려되는 상태",
    // ... 모든 설문의 모든 평가 결과 필드 포함
}
```

### 5.2. 실패 (400 Bad Request)

요청 본문의 데이터가 유효하지 않을 경우(예: 필수 필드 누락, 타입 불일치) 반환됩니다.

```json
{
    "PSQI_data": {
        "result_1": [
            "This field is required."
        ]
    }
}
```
