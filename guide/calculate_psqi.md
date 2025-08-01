# API 가이드: 수면 건강(PSQI) 점수 계산

---

## 1. Endpoint

```
POST /MentalCrowdWorkerProjectApp/app_calculate_PSQI_K/
```

## 2. 설명

요청 본문에 포함된 수면 건강(PSQI) 설문 데이터를 기반으로, PSQI-K 총점 및 각 하위 척도별 점수와 상태를 계산하여 반환합니다. 이 API는 데이터를 저장하지 않고 계산 결과만 반환합니다.

## 3. 파라미터 (Parameters)

- 없음

## 4. 요청 본문 (Request Body)

요청 본문에는 `SleepHealth` 모델의 설문 데이터 필드를 포함해야 합니다.

### 4.1. 요청 예시 (Example)

```json
{
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
```

### 4.2. 데이터 모델 (PSQI_K Request Schema)

| 필드 (Field) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- |
| `result_1` | `string` | **예 (Yes)** | 평소 수면 시작 시각 (HH:MM:SS 형식) |
| `result_2` | `integer` | **예 (Yes)** | 잠자리에 들어 수면까지 걸리는 시간 (분) |
| `result_3` | `string` | **예 (Yes)** | 평소 기상 시각 (HH:MM:SS 형식) |
| `result_4` | `integer` | **예 (Yes)** | 실제 평균 수면 시간 (분) |
| `result_5a` ~ `result_5i` | `integer` | **예 (Yes)** | 5번 문항의 각 항목 (1~4점) |
| `result_5j` | `integer` | 아니요 (No) | 5번 문항 j (기타) (1~4점) |
| `result_5j_input_text` | `string` | 아니요 (No) | 5번 문항 j의 주관식 답변 |
| `result_6` | `integer` | **예 (Yes)** | 6번 문항 (수면의 질 평가) (1~4점) |
| `result_7` | `integer` | **예 (Yes)** | 7번 문항 (수면제 사용 빈도) (1~4점) |
| `result_8` | `integer` | **예 (Yes)** | 8번 문항 (주간 졸음) (1~4점) |
| `result_9` | `integer` | **예 (Yes)** | 9번 문항 (일상생활의 어려움) (1~4점) |

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

계산된 점수와 상태가 포함된 JSON 객체를 반환합니다.

```json
{
    "sleep_quality_score": 0,
    "sleep_quality_status": "양호",
    "sleep_latency_score": 1,
    "sleep_latency_status": "양호",
    "sleep_duration_score": 0,
    "sleep_duration_status": "양호",
    "sleep_efficiency_score": 0,
    "sleep_efficiency_status": "양호",
    "sleep_disturbance_score": 1,
    "sleep_disturbance_status": "양호",
    "use_of_sleep_medication_score": 0,
    "use_of_sleep_medication_status": "없음",
    "daytime_dysfunction_score": 1,
    "daytime_dysfunction_status": "양호",
    "psqi_k": 3,
    "psqi_k_status": "숙면을 취하고 있는 상태"
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
