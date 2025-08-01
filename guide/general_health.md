# API 가이드: 일반 건강 설문 기록 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_general_health/
```

## 2. 설명

사용자들의 일반 건강(WHODAS) 설문 기록을 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 기록만, ID를 지정하지 않으면 전체 사용자의 기록을 반환합니다.

## 3. 파라미터 (Query Parameters)

| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `integer` | 아니요 (No) | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자의 기록이 배열 형태로 반환됩니다. |

## 4. 요청 예시 (Examples)

### 4.1. 전체 일반 건강 기록 조회

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_general_health/
```

### 4.2. 특정 사용자의 일반 건강 기록 조회 (ID: 1)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_general_health/?id=1
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `GeneralHealth` 객체 또는 객체의 배열이 반환됩니다.

```json
[
  {
      "id": 1,
      "participant_id": 1,
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
]
```

### 5.2. 데이터 모델 (GeneralHealth Schema)

| 필드 (Field) | 타입 (Type) | 설명 (Description) |
| :--- | :--- | :--- |
| `id` | `integer` | 일반 건강 기록의 고유 ID (PK) |
| `participant_id` | `integer` | 해당 설문을 작성한 사용자의 ID (`BasicInfo`의 PK) |
| `result_1` ~ `result_12` | `integer` | WHODAS 12문항의 각 응답 (1~5점) |
| `result_13` | `integer` | 13번 문항 (지난 30일간, 건강 문제로 인해 업무나 학업에 지장이 있었던 날의 수) (0~30) |
| `result_14` | `integer` | 14번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 적게 한 날의 수) (0~30) |
| `result_15` | `integer` | 15번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 잘하지 못한 날의 수) (0~30) |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```