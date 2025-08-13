import dotenv
dotenv.load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY는 운영 환경에서 반드시 환경 변수로 주입해야 합니다.
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
# 운영 환경에서는 DJANGO_DEBUG=False 와 같이 환경 변수를 설정해야 합니다.
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# ALLOWED_HOSTS는 운영 환경에 맞게 설정해야 합니다.
# 예: DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ALLOWED_HOSTS_STRING = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STRING.split(',')] if ALLOWED_HOSTS_STRING else []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "MentalCrowdWorkerProjectApp",
    "rest_framework"
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ]
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MentalCrowdWorkerProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, 'MentalCrowdWorkerProjectApp', 'templates'),
        ]
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = "MentalCrowdWorkerProject.wsgi.application"

# 데이터베이스 설정
# 환경 변수를 통해 데이터베이스 연결 정보를 동적으로 설정합니다.
# 기본값은 SQLite로 설정되어 있으며, 다른 DB 사용 시 환경 변수를 설정합니다.
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# static 파일을 클라이언트가 접근할 때 사용되는 URL 경로 prefix
# 예: 템플릿에서 {% static 'img/logo.png' %} → "/static/img/logo.png" 로 렌더링됨
STATIC_URL = "static/"

# collectstatic 명령어 실행 시 모든 static 파일이 이 디렉토리에 복사됨
# 배포나 PDF 생성처럼 실제 파일 경로 접근이 필요한 작업에 사용됨
# 이 경로는 직접 만들지 않아도 되고, collectstatic 실행 시 자동 생성됨
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 개발 중 Django가 static 파일을 찾기 위해 탐색할 디렉토리 목록
# 즉, 원본 static 파일들이 실제로 존재하는 위치를 명시함
# 예: MentalCrowdWorkerProjectApp/static/ 내부에 존재하는 이미지, CSS 등
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'MentalCrowdWorkerProjectApp', 'static')
]
