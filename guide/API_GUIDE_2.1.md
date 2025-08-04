# (1) API 가이드: 사용자 기본 정보 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_basic_info/
```

## 2. 설명

시스템에 등록된 사용자들의 기본 정보를 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 정보만, ID를 지정하지 않으면 전체 사용자 목록을 반환합니다.

## 3. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                    |   |
| :------------ | :------------ | :---------------- | :------------------------------------------------------------------------------------------------------ | :-- |
| `id`        | `integer`   | 아니요 (No)     | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자 정보가 배열 형태로 반환됩니다. |   |

## 4. 요청 예시 (Examples)

### 4.1. 전체 사용자 정보 조회

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_basic_info/
```

### 4.2. 특정 사용자 정보 조회 (ID: 1)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_basic_info/?id=1
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `BasicInfo` 객체 또는 객체의 배열이 반환됩니다.

- **특정 사용자 조회 시:**
  ```json
  {
    "id": 1,
    "name": "홍길동",
    "sex": 1,
    "age": 30,
    "edu_level": 4,
    "edu_level_etc": null,
    "marital_status": 2,
    "income_level": 2,
    "career_duration": 5.5,
    "task_type": 1,
    "task_description": "데이터 라벨링",
    "occupation_type": 1,
    "interest": "AI, 데이터 과학"
  }
  ```

### 5.2. 데이터 모델 (BasicInfo Schema)


| 필드 (Field)       | 타입 (Type) | 설명 (Description)                                               |
| :------------------- | :------------ | :----------------------------------------------------------------- |
| `id`               | `integer`   | 사용자의 고유 ID (PK)                                            |
| `name`             | `string`    | 사용자 이름                                                      |
| `sex`              | `integer`   | 성별 (1: 남성, 2: 여성)                                          |
| `age`              | `integer`   | 연령                                                             |
| `edu_level`        | `integer`   | 최종 학력 (1: 고졸, 2: 전문대졸, 3: 대졸, 4: 석사, 5: 박사)      |
| `edu_level_etc`    | `string`    | (선택) 최종 학력이 '기타'일 경우의 텍스트 입력                   |
| `marital_status`   | `integer`   | 결혼 상태 (1: 미혼, 2: 기혼, 3: 이혼, 4: 사별, 5: 별거, 6: 기타) |
| `income_level`     | `integer`   | 사회 경제 상태 (1: 상, 2: 중, 3: 하)                             |
| `career_duration`  | `float`     | 경력 기간 (년 단위)                                              |
| `task_type`        | `integer`   | 업무 내용 (1: 데이터 수집/가공, 2: 번역/문서작업)                |
| `task_description` | `string`    | (선택) 상세 업무 내용                                            |
| `occupation_type`  | `integer`   | 직업 형태 (1: 전업, 2: 부업, 3: 기타)                            |
| `interest`         | `string`    | (선택) 주요 관심 분야                                            |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```

# (2) API 가이드: 스트레스 요인 목록 조회

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


| 필드 (Field) | 타입 (Type) | 설명 (Description)           |
| :------------- | :------------ | :----------------------------- |
| `id`         | `integer`   | 스트레스 요인의 고유 ID (PK) |
| `type`       | `string`    | 스트레스 요인의 내용         |

### 5.3. 실패

이 API는 일반적으로 실패하지 않으나, 서버 내부 오류 발생 시 5xx 에러 코드를 반환할 수 있습니다.

# (3) API 가이드: 직업 만족도 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_job_satisfaction/
```

## 2. 설명

사용자들의 직업 만족도 설문 기록을 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 기록만, ID를 지정하지 않으면 전체 사용자의 기록을 반환합니다.

## 3. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                      |   |
| :------------ | :------------ | :---------------- | :-------------------------------------------------------------------------------------------------------- | :-- |
| `id`        | `integer`   | 아니요 (No)     | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자의 기록이 배열 형태로 반환됩니다. |   |

## 4. 요청 예시 (Examples)

### 4.1. 전체 직업 만족도 기록 조회

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_job_satisfaction/
```

### 4.2. 특정 사용자의 직업 만족도 기록 조회 (ID: 1)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_job_satisfaction/?id=1
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `JobSatisfaction` 객체 또는 객체의 배열이 반환됩니다.

```json
[
  {
      "id": 1,
      "participant_id": 1,
      "satisfaction_level": 4.5,
      "stress_factors": [2, 5]
  }
]
```

### 5.2. 데이터 모델 (JobSatisfaction Schema)


| 필드 (Field)         | 타입 (Type) | 설명 (Description)                                |
| :--------------------- | :------------ | :-------------------------------------------------- |
| `id`                 | `integer`   | 직업 만족도 기록의 고유 ID (PK)                   |
| `participant_id`     | `integer`   | 해당 설문을 작성한 사용자의 ID (`BasicInfo`의 PK) |
| `satisfaction_level` | `float`     | 업무 만족도 점수 (1.0 ~ 5.0)                      |
| `stress_factors`     | `array`     | 이 직업 만족도와 관련된`StressFactors`의 ID 목록  |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```

# (4) API 가이드: 직업 만족도-스트레스 요인 연관 데이터 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_job_satisfaction_stress_factors/
```

## 2. 설명

사용자별 직업 만족도 설문과 그에 연관된 스트레스 요인 데이터를 조회합니다. 이 API는 `JobSatisfaction`과 `StressFactors`를 연결하는 중간 테이블의 데이터를 직접 보여줍니다.

## 3. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                  |   |
| :------------ | :------------ | :---------------- | :---------------------------------------------------------------------------------------------------- | :-- |
| `id`        | `integer`   | 아니요 (No)     | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 연관 기록이 배열 형태로 반환됩니다. |   |

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


| 필드 (Field)       | 타입 (Type) | 설명 (Description)                               |
| :------------------- | :------------ | :------------------------------------------------- |
| `id`               | `integer`   | 연관 데이터의 고유 ID (PK)                       |
| `job_satisfaction` | `integer`   | `JobSatisfaction` 기록의 ID                      |
| `stress_factors`   | `integer`   | `StressFactors` 기록의 ID                        |
| `input_text`       | `string`    | (선택) 스트레스 요인에 대한 사용자의 주관식 답변 |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```

# (5) API 가이드: 수면 건강 설문 기록 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_sleep_health/
```

## 2. 설명

사용자들의 수면 건강(PSQI) 설문 기록을 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 기록만, ID를 지정하지 않으면 전체 사용자의 기록을 반환합니다.

## 3. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                      |   |
| :------------ | :------------ | :---------------- | :-------------------------------------------------------------------------------------------------------- | :-- |
| `id`        | `integer`   | 아니요 (No)     | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자의 기록이 배열 형태로 반환됩니다. |   |

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


| 필드 (Field)              | 타입 (Type) | 설명 (Description)                                |
| :-------------------------- | :------------ | :-------------------------------------------------- |
| `id`                      | `integer`   | 수면 건강 기록의 고유 ID (PK)                     |
| `participant_id`          | `integer`   | 해당 설문을 작성한 사용자의 ID (`BasicInfo`의 PK) |
| `result_1`                | `string`    | 평소 수면 시작 시각 (HH:MM:SS 형식)               |
| `result_2`                | `integer`   | 잠자리에 들어 수면까지 걸리는 시간 (분)           |
| `result_3`                | `string`    | 평소 기상 시각 (HH:MM:SS 형식)                    |
| `result_4`                | `integer`   | 실제 평균 수면 시간 (분)                          |
| `result_5a` ~ `result_5i` | `integer`   | 5번 문항의 각 항목 (1~4점)                        |
| `result_5j`               | `integer`   | (선택) 5번 문항 j (기타) (1~4점)                  |
| `result_5j_input_text`    | `string`    | (선택) 5번 문항 j의 주관식 답변                   |
| `result_6`                | `integer`   | 6번 문항 (수면의 질 평가) (1~4점)                 |
| `result_7`                | `integer`   | 7번 문항 (수면제 사용 빈도) (1~4점)               |
| `result_8`                | `integer`   | 8번 문항 (주간 졸음) (1~4점)                      |
| `result_9`                | `integer`   | 9번 문항 (일상생활의 어려움) (1~4점)              |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```

# (6) API 가이드: 일반 건강 설문 기록 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_general_health/
```

## 2. 설명

사용자들의 일반 건강(WHODAS) 설문 기록을 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 기록만, ID를 지정하지 않으면 전체 사용자의 기록을 반환합니다.

## 3. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                      |   |
| :------------ | :------------ | :---------------- | :-------------------------------------------------------------------------------------------------------- | :-- |
| `id`        | `integer`   | 아니요 (No)     | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자의 기록이 배열 형태로 반환됩니다. |   |

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


| 필드 (Field)             | 타입 (Type) | 설명 (Description)                                                                          |
| :------------------------- | :------------ | :-------------------------------------------------------------------------------------------- |
| `id`                     | `integer`   | 일반 건강 기록의 고유 ID (PK)                                                               |
| `participant_id`         | `integer`   | 해당 설문을 작성한 사용자의 ID (`BasicInfo`의 PK)                                           |
| `result_1` ~ `result_12` | `integer`   | WHODAS 12문항의 각 응답 (1~5점)                                                             |
| `result_13`              | `integer`   | 13번 문항 (지난 30일간, 건강 문제로 인해 업무나 학업에 지장이 있었던 날의 수) (0~30)        |
| `result_14`              | `integer`   | 14번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 적게 한 날의 수) (0~30)     |
| `result_15`              | `integer`   | 15번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 잘하지 못한 날의 수) (0~30) |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```

# (7) API 가이드: 감정 상태 설문 기록 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_emotion/
```

## 2. 설명

사용자들의 감정 상태(DASS-21) 설문 기록을 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 기록만, ID를 지정하지 않으면 전체 사용자의 기록을 반환합니다.

## 3. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                      |   |
| :------------ | :------------ | :---------------- | :-------------------------------------------------------------------------------------------------------- | :-- |
| `id`        | `integer`   | 아니요 (No)     | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자의 기록이 배열 형태로 반환됩니다. |   |

## 4. 요청 예시 (Examples)

### 4.1. 전체 감정 상태 기록 조회

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_emotion/
```

### 4.2. 특정 사용자의 감정 상태 기록 조회 (ID: 1)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_emotion/?id=1
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `Emotion` 객체 또는 객체의 배열이 반환됩니다.

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
      "result_13": 1,
      "result_14": 2,
      "result_15": 1,
      "result_16": 2,
      "result_17": 1,
      "result_18": 2,
      "result_19": 1,
      "result_20": 2,
      "result_21": 1
  }
]
```

### 5.2. 데이터 모델 (Emotion Schema)


| 필드 (Field)             | 타입 (Type) | 설명 (Description)                                |
| :------------------------- | :------------ | :-------------------------------------------------- |
| `id`                     | `integer`   | 감정 상태 기록의 고유 ID (PK)                     |
| `participant_id`         | `integer`   | 해당 설문을 작성한 사용자의 ID (`BasicInfo`의 PK) |
| `result_1` ~ `result_21` | `integer`   | DASS-21의 21개 문항에 대한 각 응답 (1~4점)        |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```

# (8) API 가이드: 외로움 설문 기록 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_loneliness/
```

## 2. 설명

사용자들의 외로움(LSIS) 설문 기록을 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 기록만, ID를 지정하지 않으면 전체 사용자의 기록을 반환합니다.

## 3. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                      |   |
| :------------ | :------------ | :---------------- | :-------------------------------------------------------------------------------------------------------- | :-- |
| `id`        | `integer`   | 아니요 (No)     | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자의 기록이 배열 형태로 반환됩니다. |   |

## 4. 요청 예시 (Examples)

### 4.1. 전체 외로움 기록 조회

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_loneliness/
```

### 4.2. 특정 사용자의 외로움 기록 조회 (ID: 1)

```http
GET http://127.0.0.1:8001/MentalCrowdWorkerProjectApp/app_get_loneliness/?id=1
```

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

요청에 성공하면 `Loneliness` 객체 또는 객체의 배열이 반환됩니다.

```json
[
  {
      "id": 1,
      "participant_id": 1,
      "result_1": 2,
      "result_2": 3,
      "result_3": 1,
      "result_4": 4,
      "result_5": 2,
      "result_6": 3
  }
]
```

### 5.2. 데이터 모델 (Loneliness Schema)


| 필드 (Field)            | 타입 (Type) | 설명 (Description)                                |
| :------------------------ | :------------ | :-------------------------------------------------- |
| `id`                    | `integer`   | 외로움 기록의 고유 ID (PK)                        |
| `participant_id`        | `integer`   | 해당 설문을 작성한 사용자의 ID (`BasicInfo`의 PK) |
| `result_1` ~ `result_6` | `integer`   | LSIS의 6개 문항에 대한 각 응답 (1~4점)            |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```

# (9) API 가이드: 수면 건강(PSQI) 점수 계산

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


| 필드 (Field)              | 타입 (Type) | 필수 (Required) | 설명 (Description)                      |
| :-------------------------- | :------------ | :---------------- | :---------------------------------------- |
| `result_1`                | `string`    | **예 (Yes)**    | 평소 수면 시작 시각 (HH:MM:SS 형식)     |
| `result_2`                | `integer`   | **예 (Yes)**    | 잠자리에 들어 수면까지 걸리는 시간 (분) |
| `result_3`                | `string`    | **예 (Yes)**    | 평소 기상 시각 (HH:MM:SS 형식)          |
| `result_4`                | `integer`   | **예 (Yes)**    | 실제 평균 수면 시간 (분)                |
| `result_5a` ~ `result_5i` | `integer`   | **예 (Yes)**    | 5번 문항의 각 항목 (1~4점)              |
| `result_5j`               | `integer`   | 아니요 (No)     | 5번 문항 j (기타) (1~4점)               |
| `result_5j_input_text`    | `string`    | 아니요 (No)     | 5번 문항 j의 주관식 답변                |
| `result_6`                | `integer`   | **예 (Yes)**    | 6번 문항 (수면의 질 평가) (1~4점)       |
| `result_7`                | `integer`   | **예 (Yes)**    | 7번 문항 (수면제 사용 빈도) (1~4점)     |
| `result_8`                | `integer`   | **예 (Yes)**    | 8번 문항 (주간 졸음) (1~4점)            |
| `result_9`                | `integer`   | **예 (Yes)**    | 9번 문항 (일상생활의 어려움) (1~4점)    |

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

# (10) API 가이드: 일반 건강(WHODAS) 점수 계산

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


| 필드 (Field)             | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                          |
| :------------------------- | :------------ | :---------------- | :-------------------------------------------------------------------------------------------- |
| `result_1` ~ `result_12` | `integer`   | **예 (Yes)**    | WHODAS 12문항의 각 응답 (1~5점)                                                             |
| `result_13`              | `integer`   | **예 (Yes)**    | 13번 문항 (지난 30일간, 건강 문제로 인해 업무나 학업에 지장이 있었던 날의 수) (0~30)        |
| `result_14`              | `integer`   | **예 (Yes)**    | 14번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 적게 한 날의 수) (0~30)     |
| `result_15`              | `integer`   | **예 (Yes)**    | 15번 문항 (지난 30일간, 건강 문제로 인해 평소보다 업무나 학업을 잘하지 못한 날의 수) (0~30) |

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

# (11) API 가이드: 감정 상태(DASS-21) 점수 계산

---

## 1. Endpoint

```
POST /MentalCrowdWorkerProjectApp/app_calculate_DASS21_K/
```

## 2. 설명

요청 본문에 포함된 감정 상태(DASS-21) 설문 데이터를 기반으로, 우울, 불안, 스트레스 각 하위 척도별 점수와 상태 및 총점을 계산하여 반환합니다. 이 API는 데이터를 저장하지 않고 계산 결과만 반환합니다.

## 3. 파라미터 (Parameters)

- 없음

## 4. 요청 본문 (Request Body)

요청 본문에는 `Emotion` 모델의 설문 데이터 필드를 포함해야 합니다.

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
    "result_13": 1,
    "result_14": 2,
    "result_15": 1,
    "result_16": 2,
    "result_17": 1,
    "result_18": 2,
    "result_19": 1,
    "result_20": 2,
    "result_21": 1
}
```

### 4.2. 데이터 모델 (DASS21_K Request Schema)


| 필드 (Field)             | 타입 (Type) | 필수 (Required) | 설명 (Description)                         |
| :------------------------- | :------------ | :---------------- | :------------------------------------------- |
| `result_1` ~ `result_21` | `integer`   | **예 (Yes)**    | DASS-21의 21개 문항에 대한 각 응답 (1~4점) |

## 5. 응답 (Responses)

### 5.1. 성공 (200 OK)

계산된 점수와 상태가 포함된 JSON 객체를 반환합니다.

```json
{
    "depression_score": 14,
    "depression_status": "위험",
    "anxiety_score": 14,
    "anxiety_status": "위험",
    "stress_score": 14,
    "stress_status": "양호",
    "dass": 42,
    "dass_status": "매우 심각한 상태"
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

# (12) API 가이드: 외로움(LSIS) 점수 계산

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


| 필드 (Field)            | 타입 (Type) | 필수 (Required) | 설명 (Description)                     |
| :------------------------ | :------------ | :---------------- | :--------------------------------------- |
| `result_1` ~ `result_6` | `integer`   | **예 (Yes)**    | LSIS의 6개 문항에 대한 각 응답 (1~4점) |

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

# (13) API 가이드: 전체 설문 종합 평가

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


| 필드 (Field)  | 타입 (Type) | 설명 (Description)                                                            |
| :-------------- | :------------ | :------------------------------------------------------------------------------ |
| `PSQI_data`   | `object`    | 수면 건강(PSQI) 설문 데이터 객체. 상세 스키마는`calculate_psqi.md` 참고.      |
| `WHODAS_data` | `object`    | 일반 건강(WHODAS) 설문 데이터 객체. 상세 스키마는`calculate_whodas.md` 참고.  |
| `DASS21_data` | `object`    | 감정 상태(DASS-21) 설문 데이터 객체. 상세 스키마는`calculate_dass21.md` 참고. |
| `LSIS_data`   | `object`    | 외로움(LSIS) 설문 데이터 객체. 상세 스키마는`calculate_lsis.md` 참고.         |

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

# (14) API 가이드: 리포트 조회 및 생성

---

## 1. Endpoint

```
/MentalCrowdWorkerProjectApp/report/
```

## 2. 설명

사용자의 설문 기록을 바탕으로 리포트를 조회하거나, 새로운 데이터를 기반으로 PDF 리포트를 생성하는 핵심 API입니다. `GET` 요청은 데이터 조회, `POST` 요청은 PDF 생성 및 결과 반환을 담당합니다.

---

## 3. 리포트 조회 (`GET`)

`user_id`를 기반으로 기존 리포트 데이터를 JSON 또는 HTML 형식으로 조회합니다.

### 3.1. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                                                                                                   |   |
| :------------ | :------------ | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-- |
| `id`        | `integer`   | **예 (Yes)**    | 조회할 사용자의 고유 ID입니다.                                                                                                                                                       |   |
| `html`      | `boolean`   | 아니요 (No)     | `true`로 설정 시, JSON 대신 렌더링된 HTML 보고서를 반환합니다. 이 옵션은 `mode`보다 우선순위가 높습니다.                                                                             |   |
| `mode`      | `string`    | 아니요 (No)     | `html=true`가 아닐 때, 반환될 JSON의 타입을 지정합니다.<br /><br>- `context` (기본값): 리포트의 모든 상세 데이터를 반환합니다.<br /><br>- `evaluate`: 요약된 평가 결과만 반환합니다. |   |

### 3.2. 요청 예시 (Examples)

- **상세 데이터 조회 (JSON):** `GET /report/?id=1`
- **요약 결과 조회 (JSON):** `GET /report/?id=1&mode=evaluate`
- **HTML 리포트 조회:** `GET /report/?id=1&html=true`

### 3.3. 응답 (Responses)

- **성공 (200 OK):**
  - `mode=context` (기본값): 리포트 전체 `context` 객체 (JSON)
  - `mode=evaluate`: 요약된 평가 결과 객체 (JSON)
  - `html=true`: 렌더링된 리포트 (HTML)
- **실패 (404 Not Found):** 해당 `id`의 사용자가 없을 경우

---

## 4. 리포트 생성 (`POST`)

요청 본문(Body)에 담긴 설문 데이터를 기반으로 서버에 PDF 리포트 파일을 **생성**하고, 그 결과를 다양한 형태로 반환합니다.

### 4.1. 파라미터 (Query Parameters)


| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description)                                                                                                                                                                                             |   |
| :------------ | :------------ | :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-- |
| `html`      | `boolean`   | 아니요 (No)     | `true`로 설정 시, PDF 생성 후 JSON 대신 렌더링된 HTML 보고서를 반환합니다. 이 옵션은 `mode`보다 우선순위가 높습니다.                                                                                           |   |
| `mode`      | `string`    | 아니요 (No)     | `html=true`가 아닐 때, 반환될 JSON의 타입을 지정합니다.<br /><br>- `context` (기본값): PDF 생성 후, 리포트의 모든 상세 데이터를 반환합니다.<br /><br>- `evaluate`: PDF 생성 후, 요약된 평가 결과만 반환합니다. |   |

### 4.2. 요청 본문 (Request Body)

- **Case 1: ID 기반 생성 (`ReportRequestSerializer`)**

  ```json
  {
      "id": 1,
      "pdf_path": "C:/Users/HashJam/Desktop/reports",
      "file_name": "user_1_report.pdf"
  }
  ```
- **Case 2: 전체 데이터 기반 생성 (`WholeScoresWithPathSerializer`)**

  ```json
  {
      "name": "홍길동",
      "pdf_path": "C:/Users/HashJam/Desktop/reports",
      "file_name": "new_user_report.pdf",
      "PSQI_data": { ... },
      "WHODAS_data": { ... },
      "DASS21_data": { ... },
      "LSIS_data": { ... }
  }
  ```

### 4.3. 요청 예시 (Examples)

- **PDF 생성 및 Context 반환 (기본):** `POST /report/`
- **PDF 생성 및 평가 결과 반환:** `POST /report/?mode=evaluate`
- **PDF 생성 및 HTML 반환:** `POST /report/?html=true`

### 4.4. 응답 (Responses)

- **성공 (200 OK):**
  - `mode=context` (기본값): `{"status": "success", "context": { ... }}`
  - `mode=evaluate`: `{"status": "success", "evaluation_results": { ... }}`
  - `html=true`: 렌더링된 리포트 (HTML)
- **실패 (400 Bad Request):** 요청 본문 데이터가 유효하지 않을 경우
