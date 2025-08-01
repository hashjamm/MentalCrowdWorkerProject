# API 가이드: 스트레스 요인 목록 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_stress_factors/
```

## 2. 설명

시스템에 사전 정의된 스트레스 요인들의 전체 목록을 조회합니다. 이 API는 별도의 파라미터를 받지 않습니다.

## 3. 파라미터 (Query Parameters)

- 없음

## 4. 요청 예시 (Example)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_stress_factors/
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `StressFactors` 객체의 배열이 반환됩니다.

```json
[
    {
        "id": 1,
        "type": "과도한 업무량"
    },
    {
        "id": 2,
        "type": "업무의 불확실성"
    },
    {
        "id": 3,
        "type": "대인 관계의 어려움"
    }
]
```

### 5.2. 데이터 모델 (StressFactors Schema)

| 필드 (Field) | 타입 (Type) | 설명 (Description) |
| :--- | :--- | :--- |
| `id` | `integer` | 스트레스 요인의 고유 ID (PK) |
| `type` | `string` | 스트레스 요인의 내용 |

### 5.3. 실패

이 API는 일반적으로 실패하지 않으나, 서버 내부 오류 발생 시 5xx 에러 코드를 반환할 수 있습니다.