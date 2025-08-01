# API 가이드: 사용자 기본 정보 조회

---

## 1. Endpoint

```
GET /MentalCrowdWorkerProjectApp/app_get_basic_info/
```

## 2. 설명

시스템에 등록된 사용자들의 기본 정보를 조회합니다. 특정 사용자 ID를 지정하면 해당 사용자의 정보만, ID를 지정하지 않으면 전체 사용자 목록을 반환합니다.

## 3. 파라미터 (Query Parameters)

| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `integer` | 아니요 (No) | 조회할 특정 사용자의 고유 ID입니다. 이 파라미터를 생략하면 모든 사용자 정보가 배열 형태로 반환됩니다. |

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

| 필드 (Field) | 타입 (Type) | 설명 (Description) |
| :--- | :--- | :--- |
| `id` | `integer` | 사용자의 고유 ID (PK) |
| `name` | `string` | 사용자 이름 |
| `sex` | `integer` | 성별 (1: 남성, 2: 여성) |
| `age` | `integer` | 연령 |
| `edu_level` | `integer` | 최종 학력 (1: 고졸, 2: 전문대졸, 3: 대졸, 4: 석사, 5: 박사) |
| `edu_level_etc` | `string` | (선택) 최종 학력이 '기타'일 경우의 텍스트 입력 |
| `marital_status`| `integer` | 결혼 상태 (1: 미혼, 2: 기혼, 3: 이혼, 4: 사별, 5: 별거, 6: 기타) |
| `income_level` | `integer` | 사회 경제 상태 (1: 상, 2: 중, 3: 하) |
| `career_duration`| `float` | 경력 기간 (년 단위) |
| `task_type` | `integer` | 업무 내용 (1: 데이터 수집/가공, 2: 번역/문서작업) |
| `task_description`| `string` | (선택) 상세 업무 내용 |
| `occupation_type`| `integer` | 직업 형태 (1: 전업, 2: 부업, 3: 기타) |
| `interest` | `string` | (선택) 주요 관심 분야 |

### 5.3. 실패 (404 Not Found)

요청한 `id`에 해당하는 사용자가 존재하지 않을 경우 반환됩니다.

```json
{
    "detail": "Not found."
}
```