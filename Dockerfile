# Python 3.9 베이스 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    g++ \
    wget \
    gnupg \
    fonts-noto-cjk \
    fontconfig \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Playwright 브라우저 설치
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright 브라우저 설치
RUN playwright install chromium

# 프로젝트 파일들 복사
COPY . .

# 정적 파일 수집
RUN python manage.py collectstatic --noinput

# 포트 8001 노출
EXPOSE 8001

# 환경 변수 설정
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=MentalCrowdWorkerProject.settings

# 실행 명령
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "MentalCrowdWorkerProject.wsgi"]
