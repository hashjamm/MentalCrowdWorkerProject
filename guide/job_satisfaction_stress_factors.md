# API 가이드: 직업 만족도-스트레스 요인 연관 데이터 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_job_satisfaction_stress_factors/
```

## 2. 설명

사용자별 직업 만족도 설문과 그에 연관된 스트레스 요인 데이터를 조회합니다. 이 API는 `JobSatisfaction`과 `StressFactors`를 연결하는 중간 테이블의 데이터를 직접 보여줍니다.

## 3. 파라미터 (Query Parameters)

| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `integer` | 아니요 (No) | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 연관 기록이 배열 형태로 반환됩니다. |

## 4. 요청 예시 (Examples)

### 4.1. 전체 연관 데이터 조회

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_job_satisfaction_stress_factors/
```

### 4.2. 특정 사용자의 연관 데이터 조회 (ID: 1)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_job_satisfaction_stress_factors/?id=1
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `JobSatisfactionStressFactors` 객체 또는 객체의 배열이 반환됩니다.

- **특정 사용자 조회 시:**
  ```json
  [
    [
        {
            "id": 1,
            "job_satisfaction": 1,
            "stress_factors": 2,
            "input_text": "특정 프로젝트의 마감 기한 압박"
        },
        {
            "id": 2,
            "job_satisfaction": 1,
            "stress_factors": 5,
            "input_text": null
        }
    ]
  ]
  ```

### 5.2. 데이터 모델 (JobSatisfactionStressFactors Schema)

| 필드 (Field) | 타입 (Type) | 설명 (Description) |
| :--- | :--- | :--- |
| `id` | `integer` | 연관 데이터의 고유 ID (PK) |
| `job_satisfaction` | `integer` | `JobSatisfaction` 기록의 ID |
| `stress_factors` | `integer` | `StressFactors` 기록의 ID |
| `input_text` | `string` | (선택) 스트레스 요인에 대한 사용자의 주관식 답변 |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```