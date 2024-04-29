"""
URL configuration for MentalCrowdWorkerProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from MentalCrowdWorkerProjectApp.views import BasicInfoAPIView, StressFactorsAPIView, JobSatisfactionAPIView, \
    JobSatisfactionStressFactorsAPIView, SleepHealthAPIView, GeneralHealthAPIView, EmotionAPIView, LonelinessAPIView

urlpatterns = [
    path("app_get_basic_info/", BasicInfoAPIView.as_view(), name='get'),
    path("app_get_stress_factors/", StressFactorsAPIView.as_view(), name='get'),
    path("app_get_job_satisfaction/", JobSatisfactionAPIView.as_view(), name='get'),
    path("app_get_job_satisfaction_stress_factors/", JobSatisfactionStressFactorsAPIView.as_view(), name='get'),
    path("app_get_sleep_health/", SleepHealthAPIView.as_view(), name='get'),
    path("app_get_general_health/", GeneralHealthAPIView.as_view(), name='get'),
    path("app_get_emotion/", EmotionAPIView.as_view(), name='get'),
    path("app_get_loneliness/", LonelinessAPIView.as_view(), name='get'),
    path("app_calculate_PSQI_K/", SleepHealthAPIView.as_view(), name='post'),
    path("app_calculate_WHODAS_K/", GeneralHealthAPIView.as_view(), name='post'),
    path("app_calculate_DASS21_K/", EmotionAPIView.as_view(), name='post')
]
