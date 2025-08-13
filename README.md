# MentalCrowdWorkerProject API 서버 설치 및 배포 가이드

이 문서는 MentalCrowdWorkerProject API 서버를 Docker 환경에 설치하고 배포하는 과정을 안내합니다.

## 1. 개요

본 API 서버는 Django REST Framework 기반으로 개발되었으며, 사용자 설문 데이터 처리 및 리포트 생성 기능을 제공합니다. Docker 이미지를 통해 쉽게 배포할 수 있도록 구성되어 있습니다.

## 2. 사전 준비 사항

* **Docker 설치:** 서버에 Docker Engine이 설치되어 있어야 합니다. (Docker 공식 문서 참조)
* **서버 환경:** 최소 2GB RAM, 1vCPU 이상의 리소스를 권장합니다. (운영체제: Linux 기반)

## 3. 파일 수신 및 확인

전달받은 API 서버 `tar` 파일을 서버에 업로드합니다.

* **예시:** `/home/user/docker_images/` 디렉토리에 `crowd_mental_cha_2_1.tar` 파일을 저장합니다.

## 4. 설치 및 배포 과정

### 4.1. 환경 변수 설정

API 서버는 `SECRET_KEY`, `DEBUG` 모드, `ALLOWED_HOSTS`, 데이터베이스 연결 정보 등 중요한 설정을 환경 변수로부터 읽어옵니다. 안전하고 올바른 서버 운영을 위해 다음 단계를 따라 `.env` 파일을 설정해야 합니다.

* **`.env.example` 파일 확인:** 전달받은 프로젝트 디렉토리 내에 포함된 `.env.example` 파일을 확인하여 필요한 환경 변수 목록을 파악합니다.
* **`.env` 파일 생성:** `.env.example` 파일을 복사하여 `.env` 파일을 생성합니다.

  ```bash
  cp /path/to/your/project/.env.example /path/to/your/project/.env
  ```

  (여기서 `/path/to/your/project/`는 tar 파일이 압축 해제된 프로젝트의 실제 경로를 의미합니다.)
* **`.env` 파일 내용 편집:** 생성된 `.env` 파일을 텍스트 편집기로 열어 다음 변수들을 **반드시 실제 운영 환경에 맞게 수정**합니다.

  * **`DJANGO_SECRET_KEY`**: **매우 중요!** 보안을 위해 **반드시 새로운 고유한 키를 생성하여 입력**해야 합니다. (예: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` 명령어로 생성)
  * **`DJANGO_DEBUG=False`**: **운영 환경에서는 반드시 `False`로 설정**해야 합니다. `True`로 설정 시 보안 취약점이 발생할 수 있습니다.
  * **`DJANGO_ALLOWED_HOSTS`**: API 서버가 서비스될 **실제 도메인 주소**를 쉼표(`,`)로 구분하여 입력합니다. (예: `api.yourdomain.com,yourdomain.com`)

#### 4.1.1. 데이터베이스 설정: 기본 SQLite 사용 (외부 DB 불필요 시)

기관에서 별도의 외부 데이터베이스 연결이 필요 없고, 이미지 내에 포함된 SQLite 데이터베이스만으로 충분한 경우 다음 설정을 사용합니다. 데이터베이스 조회가 필요가 없더라도, api 코드 상에서 GET 요청 등에서 충돌을 피하기 위해선 이미지 내의 SQLite 데이터베이스 연결은 필요합니다.

* `.env` 파일에서 `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` 변수들을 **설정하지 않거나 기본값 그대로 둡니다.** (기본값은 SQLite를 가리킵니다.)

  **예시 `.env` 파일 내용 (SQLite 사용 시):**

  ```
  DJANGO_SECRET_KEY='[여기에 새로 생성한 고유한 시크릿 키 입력]'
  DJANGO_DEBUG=False
  DJANGO_ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com

  # DB 관련 변수는 설정하지 않거나, .env.example의 기본값 그대로 둡니다.
  # DB_ENGINE=django.db.backends.sqlite3
  # DB_NAME=db.sqlite3
  # DB_USER=
  # DB_PASSWORD=
  # DB_HOST=
  # DB_PORT=
  ```

#### 4.1.2. 데이터베이스 설정: 외부 DB 연결 (향후 필요 시)

향후 MySQL, PostgreSQL 등 별도의 외부 데이터베이스 연결이 필요한 경우 다음 설정을 사용합니다.

* `.env` 파일에 기관에서 사용할 **실제 외부 데이터베이스의 연결 정보**를 정확하게 입력합니다.

  **예시 `.env` 파일 내용 (외부 DB 사용 시):**

  ```
  DJANGO_SECRET_KEY='[여기에 새로 생성한 고유한 시크릿 키 입력]'
  DJANGO_DEBUG=False
  DJANGO_ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com

  DB_ENGINE=django.db.backends.mysql  # 또는 django.db.backends.postgresql
  DB_NAME=your_external_database_name
  DB_USER=your_external_database_user
  DB_PASSWORD=your_external_database_password
  DB_HOST=your_external_database_host_ip_or_domain
  DB_PORT=3306 # 또는 5432 등
  ```

### 4.2. Docker 이미지 로드 및 컨테이너 실행

* **tar 파일로부터 Docker 이미지 로드:**

  ```bash
  docker load -i /home/user/docker_images/crowd_mental_cha_2_1.tar
  ```
* **로드된 이미지 확인:**

  ```bash
  docker images
  ```
* **API 서버 컨테이너 실행:**
  `.env` 파일의 환경 변수를 컨테이너에 주입하고, 외부 포트를 설정하여 컨테이너를 실행합니다.

  ```bash
  docker run -d \
    -p 8080:8001 \
    --name api_server_container \
    --env-file /path/to/your/project/.env \
    crowd_mental_cha_2_1
  ```

  * `-p 8080:8001`: 외부에서 8080 포트로 접근 시 컨테이너 내부의 8001 포트(Gunicorn이 리스닝하는 포트)로 연결됩니다. 필요에 따라 외부 포트(8080)를 변경할 수 있습니다.
  * `--env-file /path/to/your/project/.env`: 위에서 생성한 `.env` 파일의 경로를 지정하여 환경 변수를 컨테이너 내부에 주입합니다. **이 경로를 정확히 지정해야 합니다.**

### 4.3. 배포 후 추가 설정 (필수)

컨테이너가 성공적으로 실행된 후, 데이터베이스 마이그레이션과 같은 필수적인 초기 설정 작업을 수행해야 합니다.

* **컨테이너 상태 확인:**

  ```bash
  docker ps
  ```
* **데이터베이스 마이그레이션 실행 (필수):**
  컨테이너 내부에서 Django 마이그레이션을 실행하여 데이터베이스 스키마를 최신 상태로 업데이트합니다. 해당 과정에서는 이미 DB와의 연결이 완료되어 있지만, 실제 애플리케이션 코드(모델)의 기대 상태와 일치함을 확인하고, Django 내부 시스템의 일관성을 유지시켜줍니다. 실행해도 별도 데이터베이스 변동이 없으면 무해합니다.

  ```bash
  docker exec api_server_container python manage.py migrate
  ```
* **관리자 계정 생성 (선택 사항):**
  Django 관리자 페이지(`http://your_domain:8080/admin/`)에 접근하기 위한 슈퍼유저 계정이 필요하다면 생성합니다.

  ```bash
  docker exec -it api_server_container python manage.py createsuperuser
  ```

  명령어 실행 후 안내에 따라 사용자 이름, 이메일, 비밀번호를 입력합니다.
* **컨테이너 로그 확인 (문제 발생 시):**

  ```bash
  docker logs api_server_container
  ```
* **컨테이너 내부 접속 (디버깅 목적):**

  ```bash
  docker exec -it api_server_container /bin/bash
  ```

## 5. 문제 해결 (Troubleshooting)

* **컨테이너가 시작되지 않거나 오류 발생 시:**
  `docker logs api_server_container` 명령어를 사용하여 컨테이너 로그를 확인합니다. 환경 변수 설정 오류, 데이터베이스 연결 문제 등이 원인일 수 있습니다.
* **한글 깨짐 현상 (PDF 리포트):**
  `Dockerfile`에 한글 폰트가 설치되어 있는지 확인하십시오. (본 가이드에 포함된 `Dockerfile`은 Noto Sans CJK 폰트를 설치합니다.)
* **API 접근 불가:**
  * 서버 방화벽에서 컨테이너 포트(예: 8080)가 열려 있는지 확인합니다.
  * `DJANGO_ALLOWED_HOSTS` 설정이 올바른 도메인 주소를 포함하는지 확인합니다.
