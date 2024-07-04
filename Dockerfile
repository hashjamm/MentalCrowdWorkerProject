# 기반 이미지로 Python 3.9-slim을 사용
FROM python:3.9-slim

# 이미지 내에서의 작업 디렉토리 설정
WORKDIR /app

# mysqlclient 설치를 위한 종속성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 파일을 이미지로 복사
COPY requirements.txt /app/

# requirements.txt에 명시된 패키지들을 설치
RUN pip install -r requirements.txt

# 현재 디렉토리의 나머지 파일들도 이미지로 복사
COPY . /app/

# 애플리케이션 포트 설정
EXPOSE 8001

# 컨테이너 실행 시 Django 개발 서버 시작 명령어
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
