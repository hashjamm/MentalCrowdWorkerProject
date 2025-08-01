# API 가이드: 수면 건강 설문 기록 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_sleep_health/
```

## 2. 설명

사용자들의 수면 건강(PSQI) 설문 기록을 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 기록만, ID를 지정하지 않으면 전체 사용자의 기록을 반환합니다.

## 3. 파라미터 (Query Parameters)

| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `integer` | 아니요 (No) | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자의 기록이 배열 형태로 반환됩니다. |

## 4. 요청 예시 (Examples)

### 4.1. 전체 수면 건강 기록 조회

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_sleep_health/
```

### 4.2. 특정 사용자의 수면 건강 기록 조회 (ID: 1)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_sleep_health/?id=1
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `SleepHealth` 객체 또는 객체의 배열이 반환됩니다.

```json
[
  {
      "id": 1,
      "participant_id": 1,
      "result_1": "23:00:00",
      "result_2": 30,
      "result_3": "07:00:00",
      "result_4": 420,
      "result_5a": 1,
      "result_5b": 1,
      "result_5c": 1,
      "result_5d": 1,
      "result_5e": 1,
      "result_5f": 1,
      "result_5g": 1,
      "result_5h": 1,
      "result_5i": 1,
      "result_5j": null,
      "result_5j_input_text": null,
      "result_6": 1,
      "result_7": 1,
      "result_8": 1,
      "result_9": 1
  }
]
```

### 5.2. 데이터 모델 (SleepHealth Schema)

| 필드 (Field) | 타입 (Type) | 설명 (Description) |
| :--- | :--- | :--- |
| `id` | `integer` | 수면 건강 기록의 고유 ID (PK) |
| `participant_id` | `integer` | 해당 설문을 작성한 사용자의 ID (`BasicInfo`의 PK) |
| `result_1` | `string` | 평소 수면 시작 시각 (HH:MM:SS 형식) |
| `result_2` | `integer` | 잠자리에 들어 수면까지 걸리는 시간 (분) |
| `result_3` | `string` | 평소 기상 시각 (HH:MM:SS 형식) |
| `result_4` | `integer` | 실제 평균 수면 시간 (분) |
| `result_5a` ~ `result_5i` | `integer` | 5번 문항의 각 항목 (1~4점) |
| `result_5j` | `integer` | (선택) 5번 문항 j (기타) (1~4점) |
| `result_5j_input_text` | `string` | (선택) 5번 문항 j의 주관식 답변 |
| `result_6` | `integer` | 6번 문항 (수면의 질 평가) (1~4점) |
| `result_7` | `integer` | 7번 문항 (수면제 사용 빈도) (1~4점) |
| `result_8` | `integer` | 8번 문항 (주간 졸음) (1~4점) |
| `result_9` | `integer` | 9번 문항 (일상생활의 어려움) (1~4점) |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```