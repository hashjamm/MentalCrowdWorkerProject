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
from django.urls import path
from MentalCrowdWorkerProjectApp.views import (
    BasicInfoAPIView, StressFactorsAPIView, JobSatisfactionAPIView, 
    JobSatisfactionStressFactorsAPIView, SleepHealthGetView, PSQICalculateView, 
    GeneralHealthGetView, WHODASCalculateView, EmotionGetView, 
    DASS21CalculateView, LonelinessGetView, LSISCalculateView, 
    WholeSurveysCalculateView, ReportAPIView
)

urlpatterns = [
    path("app_get_basic_info/", BasicInfoAPIView.as_view(), name='get_basic_info'),
    path("app_get_stress_factors/", StressFactorsAPIView.as_view(), name='get_stress_factors'),
    path("app_get_job_satisfaction/", JobSatisfactionAPIView.as_view(), name='get_job_satisfaction'),
    path("app_get_job_satisfaction_stress_factors/", JobSatisfactionStressFactorsAPIView.as_view(), name='get_job_satisfaction_stress_factors'),
    path("app_get_sleep_health/", SleepHealthGetView.as_view(), name='get_sleep_health'),
    path("app_get_general_health/", GeneralHealthGetView.as_view(), name='get_general_health'),
    path("app_get_emotion/", EmotionGetView.as_view(), name='get_emotion'),
    path("app_get_loneliness/", LonelinessGetView.as_view(), name='get_loneliness'),
    path("app_calculate_PSQI_K/", PSQICalculateView.as_view(), name='calculate_psqi'),
    path("app_calculate_WHODAS_K/", WHODASCalculateView.as_view(), name='calculate_whodas'),
    path("app_calculate_DASS21_K/", DASS21CalculateView.as_view(), name='calculate_dass21'),
    path("app_calculate_LSIS/", LSISCalculateView.as_view(), name='calculate_lsis'),
    path("app_calculate_whole_scores/", WholeSurveysCalculateView.as_view(), name='calculate_whole_surveys'),
    path('report/', ReportAPIView.as_view(), name='report'),
]
