# API 가이드: 리포트 조회 및 생성

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

| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `integer` | **예 (Yes)** | 조회할 사용자의 고유 ID입니다. |
| `html` | `boolean` | 아니요 (No) | `true`로 설정 시, JSON 대신 렌더링된 HTML 보고서를 반환합니다. 이 옵션은 `mode`보다 우선순위가 높습니다. |
| `mode` | `string` | 아니요 (No) | `html=true`가 아닐 때, 반환될 JSON의 타입을 지정합니다.<br>- `context` (기본값): 리포트의 모든 상세 데이터를 반환합니다.<br>- `evaluate`: 요약된 평가 결과만 반환합니다. |

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

| 이름 (Name) | 타입 (Type) | 필수 (Required) | 설명 (Description) |
| :--- | :--- | :--- | :--- | :--- |
| `html` | `boolean` | 아니요 (No) | `true`로 설정 시, PDF 생성 후 JSON 대신 렌더링된 HTML 보고서를 반환합니다. 이 옵션은 `mode`보다 우선순위가 높습니다. |
| `mode` | `string` | 아니요 (No) | `html=true`가 아닐 때, 반환될 JSON의 타입을 지정합니다.<br>- `context` (기본값): PDF 생성 후, 리포트의 모든 상세 데이터를 반환합니다.<br>- `evaluate`: PDF 생성 후, 요약된 평가 결과만 반환합니다. |

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
