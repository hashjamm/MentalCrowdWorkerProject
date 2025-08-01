# API 가이드: 일반 건강(WHODAS) 점수 계산

---

## 1. Endpoint

```
POST /MentalCrowdWorkerProjectApp/app_calculate_WHODAS_K/
```

## 2. 설명

요청 본문에 포함된 일반 건강(WHODAS) 설문 데이터를 기반으로, WHODAS-K 총점 및 각 하위 척도별 점수와 상태를 계산하여 반환합니다. 이 API는 데이터를 저장하지 않고 계산 결과만 반환합니다.

## 3. 파라미터 (Parameters)

- 없음

## 4. 요청 본문 (Request Body)

요청 본문에는 `GeneralHealth` 모델의 설문 데이터 필드를 포함해야 합니다.

### 4.1. 요청 예시 (Example)

```json
{
    "result_1": 1,
    "result_2": 2,
    "result_3": 1,
    "result_4": 2,
    "result_5": 1,
    "result_6": 2,
    "result_7": 1,
    "result_8": 2,
    "result_9": 1,
    "result_10": 2,
    "result_11": 1,
    "result_12": 2,
    "result_13": 10,
    "result_14": 5,
    "result_15": 0
}
```

### 4.2. 데이터 모델 (WHODAS_K Request Schema)

| 필드 (Field) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- |
| `result_1` ~ `result_12` | `integer` | **예 (Yes)** | WHODAS 12문항의 각 응답 (1~5점) |
| `result_13` | `integer` | **예 (Yes)** | 13번 문항 (지난 30일간, 건강 문제로 인해 업무나 학업에 지장이 있었던 날의 수) (0~30) |
| `result_14` | `integer` | **예 (Yes)** | 14번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 적게 한 날의 수) (0~30) |
| `result_15` | `integer` | **예 (Yes)** | 15번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 잘하지 못한 날의 수) (0~30) |

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

계산된 점수와 상태가 포함된 JSON 객체를 반환합니다.

```json
{
    "cognition_score": 2,
    "cognition_status": "보통",
    "mobility_score": 2,
    "mobility_status": "보통",
    "self_care_score": 2,
    "self_care_status": "보통",
    "getting_along_score": 2,
    "getting_along_status": "보통",
    "life_activities_score": 2,
    "life_activities_status": "보통",
    "participation_score": 2,
    "participation_status": "보통",
    "whodas_k": 25.0,
    "whodas_k_status": "건강기능에 주의가 필요한 상태"
}
```

### 5.2. 실패 (400 Bad Request)

요청 본문의 데이터가 유효하지 않을 경우(예: 필수 필드 누락, 타입 불일치) 반환됩니다.

```json
{
    "result_1": [
        "This field is required."
    ]
}
```
