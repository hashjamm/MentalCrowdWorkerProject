# API 가이드: 외로움(LSIS) 점수 계산

---

## 1. Endpoint

```
POST /MentalCrowdWorkerProjectApp/app_calculate_LSIS/
```

## 2. 설명

요청 본문에 포함된 외로움(LSIS) 설문 데이터를 기반으로, LSIS 총점 및 각 하위 척도별 점수와 상태를 계산하여 반환합니다. 이 API는 데이터를 저장하지 않고 계산 결과만 반환합니다.

## 3. 파라미터 (Parameters)

- 없음

## 4. 요청 본문 (Request Body)

요청 본문에는 `Loneliness` 모델의 설문 데이터 필드를 포함해야 합니다.

### 4.1. 요청 예시 (Example)

```json
{
    "result_1": 2,
    "result_2": 3,
    "result_3": 1,
    "result_4": 4,
    "result_5": 2,
    "result_6": 3
}
```

### 4.2. 데이터 모델 (LSIS Request Schema)

| 필드 (Field) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- |
| `result_1` ~ `result_6` | `integer` | **예 (Yes)** | LSIS의 6개 문항에 대한 각 응답 (1~4점) |

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

계산된 점수와 상태가 포함된 JSON 객체를 반환합니다.

```json
{
    "loneliness_score": 4,
    "loneliness_status": "위험",
    "social_support_score": 4,
    "social_support_status": "위험",
    "social_network_score": 3,
    "social_network_status": "양호",
    "lsis": 11,
    "lsis_status": "사회적 관계 단절과 외로움이 우려되는 상태"
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
