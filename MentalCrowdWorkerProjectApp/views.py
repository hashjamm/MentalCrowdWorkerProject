import datetime
import os
from pathlib import Path
import re
from unittest import result
import pandas as pd  # CSV 파일 읽기용

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.template.loader import render_to_string
from django.forms import model_to_dict
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

import tempfile

from django.conf import settings
from MentalCrowdWorkerProject.settings import STATIC_ROOT
from playwright.sync_api import sync_playwright

from MentalCrowdWorkerProjectApp.models import BasicInfo, StressFactors, JobSatisfaction, JobSatisfactionStressFactors, \
    SleepHealth, GeneralHealth, Emotion, Loneliness
from MentalCrowdWorkerProjectApp.serializers import BasicInfoSerializer, StressFactorsSerializer, \
    JobSatisfactionSerializer, JobSatisfactionStressFactorsSerializer, PSQISerializer, WHODASSerializer, \
    DASS21Serializer, LSISSerializer, WholeScoresWithPathSerializer, ReportRequestSerializer, WholeScoresSerializer


# Create your views here.
class BasicInfoAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_basic_info(request)
        else:
            return self.get_personal_basic_info(request, user_id)

    def get_whole_basic_info(self, request):

        queryset = BasicInfo.objects.all()

        try:

            serializer = BasicInfoSerializer(queryset, many=True)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

    def get_personal_basic_info(self, request, user_id):

        queryset = BasicInfo.objects.get(id=user_id)

        try:

            serializer = BasicInfoSerializer(queryset)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")


class StressFactorsAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    def get(self, request):

        queryset = StressFactors.objects.all()

        try:

            serializer = StressFactorsSerializer(queryset, many=True)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("StressFactors 데이터가 존재하지 않습니다.")


class JobSatisfactionAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_job_satisfaction(request)
        else:
            return self.get_personal_job_satisfaction(request, user_id)

    def get_whole_job_satisfaction(self, request):

        queryset = JobSatisfaction.objects.all()

        try:

            serializer = JobSatisfactionSerializer(queryset, many=True)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("JobSatisfaction 데이터가 존재하지 않습니다.")

    def get_personal_job_satisfaction(self, request, user_id):

        try:

            basic_info = BasicInfo.objects.get(id=user_id)
            queryset = basic_info.job_satisfaction_set.all()

            serialized_data = JobSatisfactionSerializer(queryset, many=True).data

            return Response(serialized_data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except JobSatisfaction.DoesNotExist:

            raise NotFound("JobSatisfaction 데이터가 존재하지 않습니다.")


class JobSatisfactionStressFactorsAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_job_satisfaction_stress_factors(request)
        else:
            return self.get_personal_job_satisfaction_stress_factors(request, user_id)

    def get_whole_job_satisfaction_stress_factors(self, request):

        queryset = JobSatisfactionStressFactors.objects.all()

        try:

            serializer = JobSatisfactionStressFactorsSerializer(queryset, many=True)

            return Response(serializer.data)

        except JobSatisfactionStressFactors.DoesNotExist:

            raise NotFound("JobSatisfactionStressFactors 데이터가 존재하지 않습니다.")

    def get_personal_job_satisfaction_stress_factors(self, request, user_id):

        try:

            queryset = JobSatisfactionStressFactors.objects.filter(job_satisfaction__participant_id=user_id)
            serializer = JobSatisfactionStressFactorsSerializer(queryset, many=True)
            result = serializer.data

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:

            return Response({"error": "서버 내부 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SleepHealthBaseView(APIView):

    @staticmethod
    def evaluate_sleep_health(records):
        result_list = []
        for one_record in records:

            # one_record 의 딕셔너리화 인스턴스를 미리 생성
            # (미리 생성하지 않으면 이후에 one_record 를 scaling 하기 때문에 문제가 발생할 수 있음)
            record_dict = model_to_dict(one_record)

            # Scaling
            elements_to_rescaling = ['result_5a', 'result_5b', 'result_5c', 'result_5d',
                                     'result_5e', 'result_5f', 'result_5g', 'result_5h',
                                     'result_5i', 'result_5j', 'result_6', 'result_7',
                                     'result_8', 'result_9']

            for element in elements_to_rescaling:
                current_value = getattr(one_record, element)
                setattr(one_record, element, current_value - 1)

            # Define scoring conditions
            c1 = one_record.result_6

            c2_element_1 = 3 if one_record.result_2 > 60 else 2 if one_record.result_2 > 30 else 1 if one_record.result_2 > 15 else 0
            pre_c2 = c2_element_1 + one_record.result_5a
            c2 = 3 if pre_c2 >= 5 else 2 if pre_c2 >= 3 else 1 if pre_c2 >= 1 else 0

            c3 = 0 if one_record.result_4 > 420 else 1 if one_record.result_4 > 360 else 2 if one_record.result_4 > 300 else 3

            arbitrary_day = datetime.datetime.today().date()
            # 하나의 하루를 추가합니다.
            next_day = arbitrary_day + datetime.timedelta(days=1)

            datetime_result_3 = datetime.datetime.combine(next_day, one_record.result_3)
            datetime_result_1 = datetime.datetime.combine(arbitrary_day, one_record.result_1)
            pre_c4 = (one_record.result_4 / ((datetime_result_3 - datetime_result_1).total_seconds() / 60)) * 100
            c4 = 3 if pre_c4 < 65 else 2 if pre_c4 < 75 else 1 if pre_c4 < 85 else 0

            pre_c5 = sum([one_record.result_5b, one_record.result_5c, one_record.result_5d, one_record.result_5e,
                          one_record.result_5f, one_record.result_5g, one_record.result_5h, one_record.result_5i,
                          one_record.result_5j])
            c5 = 3 if pre_c5 > 18 else 2 if pre_c5 > 9 else 1 if pre_c5 > 0 else 0

            c6 = one_record.result_7

            pre_c7 = one_record.result_8 + one_record.result_9
            c7 = 3 if pre_c7 > 4 else 2 if pre_c7 > 2 else 1 if pre_c7 > 0 else 0

            psqi_k = sum([c1, c2, c3, c4, c5, c6, c7])

            psqi_k_status = "숙면을 취하고 있는 상태" if psqi_k <= 4 else "수면 건강에 주의가 필요한 상태" if psqi_k <= 10 else "수면 건강이 위험한 상태"

            # 주희쌤께서 전달 주신 각 세부 항목별 점수에 대한 상태 기준에 따름. 공인된 것인지는 모르겠음
            sleep_quality_status = "양호" if c1 < 2 else "위험"
            sleep_latency_status = "양호" if c2 < 2 else "주의" if c2 == 2 else "위험"
            sleep_duration_status = "양호" if c3 < 1 else "주의" if c3 == 1 or c3 == 2 else "위험"
            sleep_efficiency_status = "양호" if c3 < 2 else "주의" if c4 == 2 else "위험"
            sleep_disturbance_status = "양호" if c5 < 2 else "주의" if c5 == 2 else "위험"
            use_of_sleep_medication_status = "없음" if c6 == 0 else "주당 1회" if c6 == 1 else "주당 2회" if c6 == 2 else "주당 3회 이상"
            daytime_dysfunction_status = "양호" if c7 < 2 else "위험"

            record_dict['sleep_quality_score'] = c1
            record_dict['sleep_quality_status'] = sleep_quality_status
            record_dict['sleep_latency_score'] = c2
            record_dict['sleep_latency_status'] = sleep_latency_status
            record_dict['sleep_duration_score'] = c3
            record_dict['sleep_duration_status'] = sleep_duration_status
            record_dict['sleep_efficiency_score'] = c4
            record_dict['sleep_efficiency_status'] = sleep_efficiency_status
            record_dict['sleep_disturbance_score'] = c5
            record_dict['sleep_disturbance_status'] = sleep_disturbance_status
            record_dict['use_of_sleep_medication_score'] = c6
            record_dict['use_of_sleep_medication_status'] = use_of_sleep_medication_status
            record_dict['daytime_dysfunction_score'] = c7
            record_dict['daytime_dysfunction_status'] = daytime_dysfunction_status
            record_dict['psqi_k'] = psqi_k
            record_dict['psqi_k_status'] = psqi_k_status

            result_list.append(record_dict)

        return result_list

    def get_whole_sleep_health(self, request):
        queryset = SleepHealth.objects.all()
        result_list = self.evaluate_sleep_health(queryset)
        return Response(result_list, status=status.HTTP_200_OK)

    def get_personal_sleep_health(self, request, user_id):
        # get_object_or_404를 사용하여 BasicInfo가 없으면 404 에러를 자동으로 반환
        basic_info = get_object_or_404(BasicInfo, id=user_id)
        queryset = basic_info.sleep_health_set.all()
        result_list = self.evaluate_sleep_health(queryset)
        return Response(result_list, status=status.HTTP_200_OK)

class SleepHealthGetView(SleepHealthBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_sleep_health(request)
        else:
            return self.get_personal_sleep_health(request, user_id)

class PSQICalculateView(SleepHealthBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    def post(self, request):

        serialized_data = PSQISerializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = SleepHealth(**serialized_data.validated_data)
            input_data = [instance]
            result = self.evaluate_sleep_health(input_data)

            keys_to_extract = ['sleep_quality_score', 'sleep_quality_status',
                               'sleep_latency_score', 'sleep_latency_status',
                               'sleep_duration_score', 'sleep_duration_status',
                               'sleep_efficiency_score', 'sleep_efficiency_status',
                               'sleep_disturbance_score', 'sleep_disturbance_status',
                               'use_of_sleep_medication_score', 'use_of_sleep_medication_status',
                               'daytime_dysfunction_score', 'daytime_dysfunction_status',
                               'psqi_k', 'psqi_k_status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class GeneralHealthBaseView(APIView):

    @staticmethod
    def evaluate_general_health(records):
        result_list = []
        for one_record in records:

            # one_record 의 딕셔너리화 인스턴스를 미리 생성
            # (미리 생성하지 않으면 이후에 one_record 를 scaling 하기 때문에 문제가 발생할 수 있음)
            record_dict = model_to_dict(one_record)

            # Define scoring conditions
            # c1: 인지, c2: 이동성, c3: 자기 관리, c4: 대인 관계, c5: 생활 활동, c6: 사회 참여

            # Scaling
            elements_to_rescaling = ['result_1', 'result_2', 'result_3', 'result_4',
                                     'result_5', 'result_6', 'result_7', 'result_8',
                                     'result_9', 'result_10', 'result_11', 'result_12']

            for element in elements_to_rescaling:
                current_value = getattr(one_record, element)
                setattr(one_record, element, current_value - 1)

            c1 = one_record.result_3 + one_record.result_6
            c2 = one_record.result_1 + one_record.result_7
            c3 = one_record.result_8 + one_record.result_9
            c4 = one_record.result_10 + one_record.result_11
            c5 = one_record.result_2 + one_record.result_12
            c6 = one_record.result_4 + one_record.result_5

            whodas_k = round(100 * (c1 + c2 + c3 + c4 + c5 + c6) / 48, 2)

            whodas_k_status = "매우 양호한 상태" if whodas_k < 18 \
                else "건강기능에 주의가 필요한 상태" if whodas_k < 31 \
                else "건강기능에 어려움이 있는 상태" if whodas_k < 43 \
                else "건강기능이 위험한 상태" if whodas_k < 61 \
                else "건강기능에 심각한 위험이 있는 상태"

            # 주희쌤께서 전달 주신 각 세부 항목별 점수에 대한 상태 기준에 따름. 공인된 것인지는 모르겠음
            cognition_status = "양호" if c1 < 2 else "보통" if c1 < 4 else "주의" if c1 < 6 else "위험"
            mobility_status = "양호" if c2 < 2 else "보통" if c2 < 4 else "주의" if c2 < 6 else "위험"
            self_care_status = "양호" if c3 < 2 else "보통" if c3 < 4 else "주의" if c3 < 6 else "위험"
            getting_along_status = "양호" if c4 < 2 else "보통" if c4 < 4 else "주의" if c4 < 6 else "위험"
            life_activities_status = "양호" if c5 < 2 else "보통" if c5 < 4 else "주의" if c5 < 6 else "위험"
            participation_status = "양호" if c6 < 2 else "보통" if c6 < 4 else "주의" if c6 < 6 else "위험"

            record_dict['cognition_score'] = c1
            record_dict['cognition_status'] = cognition_status
            record_dict['mobility_score'] = c2
            record_dict['mobility_status'] = mobility_status
            record_dict['self_care_score'] = c3
            record_dict['self_care_status'] = self_care_status
            record_dict['getting_along_score'] = c4
            record_dict['getting_along_status'] = getting_along_status
            record_dict['life_activities_score'] = c5
            record_dict['life_activities_status'] = life_activities_status
            record_dict['participation_score'] = c6
            record_dict['participation_status'] = participation_status
            record_dict['whodas_k'] = whodas_k
            record_dict['whodas_k_status'] = whodas_k_status

            result_list.append(record_dict)

        return result_list

    def get_whole_general_health(self, request):
        queryset = self.objects.all()
        result_list = self.evaluate_general_health(queryset)
        return Response(result_list, status=status.HTTP_200_OK)

    def get_personal_general_health(self, request, user_id):
        # get_object_or_404를 사용하여 BasicInfo가 없으면 404 에러를 자동으로 반환
        basic_info = get_object_or_404(BasicInfo, id=user_id)
        queryset = basic_info.general_health_set.all()
        result_list = self.evaluate_general_health(queryset)
        return Response(result_list, status=status.HTTP_200_OK)

class GeneralHealthGetView(GeneralHealthBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_general_health(request)
        else:
            return self.get_personal_general_health(request, user_id)

class WHODASCalculateView(GeneralHealthBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    def post(self, request):

        serialized_data = WHODASSerializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = GeneralHealth(**serialized_data.validated_data)
            input_data = [instance]
            result = self.evaluate_general_health(input_data)

            keys_to_extract = ['cognition_score', 'cognition_status',
                               'mobility_score', 'mobility_status',
                               'self_care_score', 'self_care_status',
                               'getting_along_score', 'getting_along_status',
                               'life_activities_score', 'life_activities_status',
                               'participation_score', 'participation_status',
                               'whodas_k', 'whodas_k_status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class EmotionBaseView(APIView):

    @staticmethod
    def evaluate_emotion(records):
        result_list = []
        for one_record in records:

            # one_record 의 딕셔너리화 인스턴스를 미리 생성
            # (미리 생성하지 않으면 이후에 one_record 를 scaling 하기 때문에 문제가 발생할 수 있음)
            record_dict = model_to_dict(one_record)

            # Define scoring conditions
            # c1: Depression Scale, c2: Anxiety Scale, c3: Stress Scale

            # Scaling
            elements_to_rescaling = ['result_1', 'result_2', 'result_3', 'result_4', 'result_5',
                                     'result_6', 'result_7', 'result_8', 'result_9', 'result_10',
                                     'result_11', 'result_12', 'result_13', 'result_14', 'result_15',
                                     'result_16', 'result_17', 'result_18', 'result_19', 'result_20',
                                     'result_21']

            for element in elements_to_rescaling:
                current_value = getattr(one_record, element)
                setattr(one_record, element, current_value - 1)

            c1_list = [one_record.result_1, one_record.result_2, one_record.result_4, one_record.result_6,
                       one_record.result_7, one_record.result_8, one_record.result_9, one_record.result_11,
                       one_record.result_12, one_record.result_14, one_record.result_15, one_record.result_18,
                       one_record.result_19, one_record.result_20]
            c2_list = [one_record.result_1, one_record.result_3, one_record.result_5, one_record.result_6,
                       one_record.result_8, one_record.result_10, one_record.result_11, one_record.result_12,
                       one_record.result_13, one_record.result_14, one_record.result_16, one_record.result_17,
                       one_record.result_18, one_record.result_21]
            c3_list = [one_record.result_2, one_record.result_3, one_record.result_4, one_record.result_5,
                       one_record.result_7, one_record.result_9, one_record.result_10, one_record.result_13,
                       one_record.result_15, one_record.result_16, one_record.result_17, one_record.result_19,
                       one_record.result_20, one_record.result_21]

            c1 = sum(c1_list)
            c2 = sum(c2_list)
            c3 = sum(c3_list)

            # 총점에 대한 상태 반환 추가
            dass = c1 + c2 + c3
            dass_status = "정서적으로 건강한 상태" if dass < 15 \
                else "가벼운 정서적 어려움이 있는 상태" if dass < 21 \
                else "중간단계의 정서적 어려움이 있는 상태" if dass < 30 \
                else "심각한 정서적 어려움이 있는 상태" if dass < 39 \
                else "매우 심각한 상태"

            depression_status = "양호" if c1 < 10 else "주의" if c1 < 14 else "위험" if c1 < 21 \
                else "심각" if c1 < 28 else "매우 심각"
            anxiety_status = "양호" if c2 < 8 else "주의" if c2 < 10 else "위험" if c2 < 15 \
                else "심각" if c2 < 20 else "매우 심각"
            stress_status = "양호" if c3 < 15 else "주의" if c3 < 19 else "위험" if c3 < 26 \
                else "심각" if c3 < 34 else "매우 심각"

            record_dict['depression_score'] = c1
            record_dict['depression_status'] = depression_status
            record_dict['anxiety_score'] = c2
            record_dict['anxiety_status'] = anxiety_status
            record_dict['stress_score'] = c3
            record_dict['stress_status'] = stress_status
            record_dict['dass'] = dass
            record_dict['dass_status'] = dass_status

            result_list.append(record_dict)

        return result_list

    def get_whole_emotion(self, request):
        queryset = Emotion.objects.all()
        result_list = self.evaluate_emotion(queryset)
        return Response(result_list, status=status.HTTP_200_OK)

    def get_personal_emotion(self, request, user_id):
        # get_object_or_404를 사용하여 BasicInfo가 없으면 404 에러를 자동으로 반환
        basic_info = get_object_or_404(BasicInfo, id=user_id)
        queryset = basic_info.emotion_set.all()
        result_list = self.evaluate_emotion(queryset)
        return Response(result_list, status=status.HTTP_200_OK)

class EmotionGetView(EmotionBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_emotion(request)
        else:
            return self.get_personal_emotion(request, user_id)

class DASS21CalculateView(EmotionBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    def post(self, request):

        serialized_data = DASS21Serializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = Emotion(**serialized_data.validated_data)
            input_data = [instance]
            result = self.evaluate_emotion(input_data)

            keys_to_extract = ['depression_score', 'depression_status',
                               'anxiety_score', 'anxiety_status',
                               'stress_score', 'stress_status',
                               'dass', 'dass_status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class LonelinessBaseView(APIView):

    @staticmethod
    def evaluate_loneliness(records):
        result_list = []
        for one_record in records:

            # one_record 의 딕셔너리화 인스턴스를 미리 생성
            # (미리 생성하지 않으면 이후에 one_record 를 scaling 하기 때문에 문제가 발생할 수 있음)
            record_dict = model_to_dict(one_record)

            # Define scoring conditions
            # c1: Loneliness Scale, c2: Social Support Scale, c3: Stress Network Scale

            # Scaling
            elements_to_rescaling = ['result_1', 'result_2', 'result_3',
                                     'result_4', 'result_5', 'result_6']

            for element in elements_to_rescaling:
                current_value = getattr(one_record, element)
                setattr(one_record, element, current_value - 1)

            c1_list = [one_record.result_1, one_record.result_2]
            c2_list = [one_record.result_3, one_record.result_4]
            c3_list = [one_record.result_5, one_record.result_6]

            c1 = sum(c1_list)

            c2 = 0
            c3 = 0

            for i, e in zip(c2_list, c3_list):
                c2 += (3 - i)
                c3 += (3 - e)

            lsis = c1 + c2 + c3
            lsis_status = "사회적 관계가 건강한 상태" if lsis < 9 else "사회적 관계 단절과 외로움이 우려되는 상태"

            loneliness_status = "양호" if c1 < 3 else "위험"
            social_support_status = "양호" if c2 < 4 else "위험"
            social_network_status = "양호" if c3 < 4 else "위험"

            record_dict['loneliness_score'] = c1
            record_dict['loneliness_status'] = loneliness_status
            record_dict['social_support_score'] = c2
            record_dict['social_support_status'] = social_support_status
            record_dict['social_network_score'] = c3
            record_dict['social_network_status'] = social_network_status
            record_dict['lsis'] = lsis
            record_dict['lsis_status'] = lsis_status

            result_list.append(record_dict)

        return result_list

    def get_whole_loneliness(self, request):
        queryset = Loneliness.objects.all()
        result_list = self.evaluate_loneliness(queryset)
        return Response(result_list, status=status.HTTP_200_OK)

    def get_personal_loneliness(self, request, user_id):
        # get_object_or_404를 사용하여 BasicInfo가 없으면 404 에러를 자동으로 반환
        basic_info = get_object_or_404(BasicInfo, id=user_id)
        queryset = basic_info.loneliness_set.all()
        result_list = self.evaluate_loneliness(queryset)
        return Response(result_list)

class LonelinessGetView(LonelinessBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_loneliness(request)
        else:
            return self.get_personal_loneliness(request, user_id)

class LSISCalculateView(LonelinessBaseView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    def post(self, request):

        serialized_data = LSISSerializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = Loneliness(**serialized_data.validated_data)
            input_data = [instance]
            result = self.evaluate_loneliness(input_data)

            keys_to_extract = ['loneliness_score', 'loneliness_status',
                               'social_support_score', 'social_support_status',
                               'social_network_score', 'social_network_status',
                               'lsis', 'lsis_status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

class WholeSurveysCalculateView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def evaluate_surveys_from_data(validated_data):
        """
        validated_data를 기반으로 모든 설문을 평가하고 결과를 병합하여 반환합니다.
        이 로직은 WholeSurveysAPIView.post에서 분리되어 다른 곳에서도 재사용 가능합니다.
        """
        # 제공된 데이터에서 각 설문 데이터 추출
        PSQI_data = validated_data.get('PSQI_data', {})
        WHODAS_data = validated_data.get('WHODAS_data', {})
        DASS21_data = validated_data.get('DASS21_data', {})
        LSIS_data = validated_data.get('LSIS_data', {})

        sub_dict1, sub_dict2, sub_dict3, sub_dict4 = {}, {}, {}, {}

        # 각 설문 데이터로 모델 인스턴스 생성 및 평가
        if PSQI_data:
            psqi_instance = SleepHealth(**PSQI_data)
            psqi_result = SleepHealthBaseView.evaluate_sleep_health([psqi_instance])[0]
            keys_to_extract = ['sleep_quality_score', 'sleep_quality_status',
                               'sleep_latency_score', 'sleep_latency_status',
                               'sleep_duration_score', 'sleep_duration_status',
                               'sleep_efficiency_score', 'sleep_efficiency_status',
                               'sleep_disturbance_score', 'sleep_disturbance_status',
                               'use_of_sleep_medication_score', 'use_of_sleep_medication_status',
                               'daytime_dysfunction_score', 'daytime_dysfunction_status',
                               'psqi_k', 'psqi_k_status']
            sub_dict1 = {key: psqi_result[key] for key in keys_to_extract if key in psqi_result}

        if WHODAS_data:
            whodas_instance = GeneralHealth(**WHODAS_data)
            whodas_result = GeneralHealthBaseView.evaluate_general_health([whodas_instance])[0]
            keys_to_extract = ['cognition_score', 'cognition_status',
                               'mobility_score', 'mobility_status',
                               'self_care_score', 'self_care_status',
                               'getting_along_score', 'getting_along_status',
                               'life_activities_score', 'life_activities_status',
                               'participation_score', 'participation_status',
                               'whodas_k', 'whodas_k_status']
            sub_dict2 = {key: whodas_result[key] for key in keys_to_extract if key in whodas_result}

        if DASS21_data:
            dass_instance = Emotion(**DASS21_data)
            dass_result = EmotionBaseView.evaluate_emotion([dass_instance])[0]
            keys_to_extract = ['depression_score', 'depression_status',
                               'anxiety_score', 'anxiety_status',
                               'stress_score', 'stress_status',
                               'dass', 'dass_status']
            sub_dict3 = {key: dass_result[key] for key in keys_to_extract if key in dass_result}

        if LSIS_data:
            lsis_instance = Loneliness(**LSIS_data)
            lsis_result = LonelinessBaseView.evaluate_loneliness([lsis_instance])[0]
            keys_to_extract = ['loneliness_score', 'loneliness_status',
                               'social_support_score', 'social_support_status',
                               'social_network_score', 'social_network_status',
                               'lsis', 'lsis_status']
            sub_dict4 = {key: lsis_result[key] for key in keys_to_extract if key in lsis_result}

        return sub_dict1 | sub_dict2 | sub_dict3 | sub_dict4

    def post(self, request):
        serializer = WholeScoresSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            merged_dict = self.evaluate_surveys_from_data(serializer.validated_data)
            return Response(merged_dict, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'An error occurred during evaluation: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ReportAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    @staticmethod
    def _extract_evaluation_results(context: dict) -> dict:
        """
        Extracts a flat dictionary of evaluation results from the main report context.
        This is for GET requests with mode=evaluate, to match the POST evaluation structure.
        """
        # Define the keys for each survey type
        psqi_keys = [
            'sleep_quality_score', 'sleep_quality_status', 'sleep_latency_score', 'sleep_latency_status',
            'sleep_duration_score', 'sleep_duration_status', 'sleep_efficiency_score', 'sleep_efficiency_status',
            'sleep_disturbance_score', 'sleep_disturbance_status', 'use_of_sleep_medication_score',
            'use_of_sleep_medication_status', 'daytime_dysfunction_score', 'daytime_dysfunction_status',
            'psqi_k', 'psqi_k_status'
        ]
        whodas_keys = [
            'cognition_score', 'cognition_status', 'mobility_score', 'mobility_status',
            'self_care_score', 'self_care_status', 'getting_along_score', 'getting_along_status',
            'life_activities_score', 'life_activities_status', 'participation_score', 'participation_status',
            'whodas_k', 'whodas_k_status'
        ]
        dass_keys = [
            'depression_score', 'depression_status', 'anxiety_score', 'anxiety_status',
            'stress_score', 'stress_status', 'dass', 'dass_status'
        ]
        lsis_keys = [
            'loneliness_score', 'loneliness_status', 'social_support_score', 'social_support_status',
            'social_network_score', 'social_network_status', 'lsis', 'lsis_status'
        ]

        # Extract the data from the context
        results = {}
        for key in psqi_keys + whodas_keys + dass_keys + lsis_keys:
            if key in context:
                results[key] = context[key]
        
        return results

    def get(self, request):
        user_id = request.query_params.get('id')
        mode = request.query_params.get('mode', 'context') # Default to 'context'
        html_option = request.query_params.get('html', 'false').lower() == 'true'

        if not user_id:
            return Response({'error': 'user_id는 필수 파라미터입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Build the full context once.
            context = self.build_report_context_from_id(user_id)

            # HTML response has top priority.
            if html_option:
                html = render_to_string("report_template.html", context)
                return HttpResponse(html)

            # If not HTML, handle JSON responses based on mode.
            if mode == 'evaluate':
                evaluation_results = self._extract_evaluation_results(context)
                return Response(evaluation_results)
            
            # Default case (mode='context' or any other value)
            return Response(context)

        except NotFound:
             return Response({'error': f'ID {user_id}에 해당하는 사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {'error': '서버 내부 오류로 리포트 조회에 실패했습니다.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        mode = request.query_params.get('mode', 'context')
        html_option = request.query_params.get('html', 'false').lower() == 'true'
        request_data = request.data

        try:
            if 'id' in request_data:
                serializer_class = ReportRequestSerializer
                generation_func = self.generate_report_pdf_from_id
            else:
                serializer_class = WholeScoresWithPathSerializer
                generation_func = self.generate_report_pdf_from_data

            serializer = serializer_class(data=request_data)
            if not serializer.is_valid():
                return Response(
                    {'error': '잘못된 요청 데이터입니다.', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            validated_data = serializer.validated_data

            # Context is needed for HTML or any JSON response.
            is_context_needed = True

            # Generate PDF and get context back.
            result_context = generation_func(validated_data, context_option=is_context_needed)

            # HTML response has top priority.
            if html_option:
                html = render_to_string("report_template.html", result_context)
                return HttpResponse(html)

            # Handle JSON responses based on mode.
            if mode == 'evaluate':
                if 'id' in validated_data:
                    return Response(
                        {'error': "mode=evaluate는 'id'와 함께 사용할 수 없습니다. 전체 설문 데이터를 제공해주세요."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                evaluation_results = self._extract_evaluation_results(result_context)
                return Response({
                    'status': 'success',
                    'evaluation_results': evaluation_results
                }, status=status.HTTP_200_OK)
            
            # Default case (mode='context').
            return Response({'status': 'success', 'context': result_context}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': '서버 내부 오류로 리포트 생성에 실패했습니다.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def load_description(relative_path, name=None, score=None, score_status=None, score1=None, status1=None,
                         score2=None, status2=None, score3=None, status3=None, score4=None, status4=None,
                         score5=None, status5=None, score6=None, status6=None, score7=None, status7=None,
                         psqi_k_status=None, whodas_k_status=None, dass_status=None, lsis_status=None,
                         assessment_results_summary_refined=None):

        # 앱 디렉토리 기준 경로 구성
        app_path = Path(apps.get_app_config('MentalCrowdWorkerProjectApp').path)
        file_path = app_path / relative_path

        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} 파일이 존재하지 않습니다.")

        text = file_path.read_text(encoding='utf-8')

        # ✅ 치환할 placeholder 딕셔너리 구성
        placeholders = {
            "name": name,
            "score": str(score) if score is not None else None,
            "score_status": score_status,
            "score1": str(score1) if score1 is not None else None,
            "status1": status1,
            "score2": str(score2) if score2 is not None else None,
            "status2": status2,
            "score3": str(score3) if score3 is not None else None,
            "status3": status3,
            "score4": str(score4) if score4 is not None else None,
            "status4": status4,
            "score5": str(score5) if score5 is not None else None,
            "status5": status5,
            "score6": str(score6) if score6 is not None else None,
            "status6": status6,
            "score7": str(score7) if score7 is not None else None,
            "status7": status7,
            "psqi_k_status": psqi_k_status,
            "whodas_k_status": whodas_k_status,
            "dass_status": dass_status,
            "lsis_status": lsis_status,
            "assessment_results_summary_refined": assessment_results_summary_refined,
        }

        # ✅ placeholder 치환
        for key, value in placeholders.items():
            if value is not None:
                text = text.replace(f"{{{{{key}}}}}", value)

        # ✅ 강조 문법 변환
        # **텍스트** → <span style="color:#FFA500;"><strong>텍스트</strong></span>
        text = re.sub(r'\*\*(.*?)\*\*', r'<span style="color:#FFA500;"><strong>\1</strong></span>', text)

        # *텍스트* → <strong>텍스트</strong>
        text = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', text)

        return text

    @staticmethod
    def load_csv_data(file_name, has_header=True):
        """
        CSV 파일을 pandas DataFrame으로 읽어옵니다.
        
        Args:
            file_name (str): CSV 파일명
            has_header (bool): 헤더 포함 여부 (기본값: True)
        
        Returns:
            pd.DataFrame: CSV 데이터를 담은 DataFrame
        """
        
        csv_path = os.path.join(
            settings.BASE_DIR,
            'MentalCrowdWorkerProjectApp',
            'data',
            file_name,
        )
        
        try:
            if has_header:
                # 헤더가 있는 경우
                df = pd.read_csv(csv_path, encoding='utf-8')
            else:
                # 헤더가 없는 경우
                df = pd.read_csv(csv_path, encoding='utf-8', header=None)
            
            return df
            
        except FileNotFoundError:
            print(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
            return pd.DataFrame()  # 빈 DataFrame 반환
        except Exception as e:
            print(f"CSV 파일 읽기 오류: {e}")
            return pd.DataFrame()  # 빈 DataFrame 반환

    @staticmethod
    def summary_refined(psqi_k_status=None, whodas_k_status=None, dass_status=None, lsis_status=None):
        """
        종합적인 평가를 생성합니다。
        """
        df = ReportAPIView.load_csv_data('health_status_summary_table.csv')
        
        # CSV 파일이 비어있거나 로드되지 않은 경우 오류 발생
        if df.empty:
            raise ValueError("health_status_summary_table.csv 파일이 비어있거나 로드할 수 없습니다.")
        
        def find_index_safe_for_code(lst, value):
            try:
                return lst.index(value) + 1
            except ValueError:
                return 0
        
        psqi_status_k_list = ["숙면을 취하고 있는 상태", "수면 건강에 주의가 필요한 상태", "수면 건강이 위험한 상태"] # 수면 건강
        whodas_k_status_list = ["매우 양호한 상태", "건강기능에 주의가 필요한 상태", "건강기능에 어려움이 있는 상태", "건강기능이 위험한 상태", "건강기능에 심각한 위험이 있는 상태"] # 신체 건강
        dass_status_list = ["정서적으로 건강한 상태", "가벼운 정서적 어려움이 있는 상태", "중간단계의 정서적 어려움이 있는 상태", "심각한 정서적 어려움이 있는 상태", "매우 심각한 상태"] # 정신 건강
        lsis_status_list = ["사회적 관계가 건강한 상태", "사회적 관계 단절과 외로움이 우려되는 상태"] # 사회적 관계

        psqi_k_num = find_index_safe_for_code(psqi_status_k_list, psqi_k_status)
        whodas_k_num = find_index_safe_for_code(whodas_k_status_list, whodas_k_status)
        dass_num = find_index_safe_for_code(dass_status_list, dass_status)
        lsis_num = find_index_safe_for_code(lsis_status_list, lsis_status)

        code = psqi_k_num*1000 + whodas_k_num*100 + dass_num*10 + lsis_num
        
        # CSV에서 해당 code의 refined_summary 값 찾기
        matching_rows = df[df['code'] == code]
        
        if not matching_rows.empty:
            # 첫 번째 매칭되는 행의 refined_summary 값 반환
            result = matching_rows.iloc[0]['refined_summary']
            return result
        else:
            # 해당 code가 없으면 오류 발생
            raise ValueError(f"코드 {code}에 해당하는 요약 정보를 찾을 수 없습니다. CSV 파일을 확인해주세요.")

    @staticmethod
    def _build_context_from_evaluated_results(psqi_result: dict, whodas_result: dict, dass_result: dict, lsis_result: dict, name: str) -> dict:
        """
        평가된 결과들을 바탕으로 리포트 context를 생성하는 공통 헬퍼 함수입니다.
        """
        # 최종 결과 점수
        psqi_k = psqi_result.get('psqi_k', 0)
        whodas_k = whodas_result.get('whodas_k', 0)
        dass = dass_result.get('dass', 0)
        lsis = lsis_result.get('lsis', 0)

        # 최종 결과 점수 백분율
        psqi_k_percent = round(psqi_k / 21 * 100, 2)
        whodas_k_percent = round(whodas_k / 100 * 100, 2)
        dass_percent = round(dass / 126 * 100, 2)
        lsis_percent = round(lsis / 18 * 100, 2)

        # 최종 결과 점수 상태
        psqi_k_status = psqi_result.get('psqi_k_status', '')
        whodas_k_status = whodas_result.get('whodas_k_status', '')
        dass_status = dass_result.get('dass_status', '')
        lsis_status = lsis_result.get('lsis_status', '')
    
        assessment_results_summary_refined = ReportAPIView.summary_refined(
            psqi_k_status=psqi_k_status,
            whodas_k_status=whodas_k_status,
            dass_status=dass_status,
            lsis_status=lsis_status)

        # 수면 세부 점수
        sleep_quality_score = psqi_result.get('sleep_quality_score', 0)
        sleep_latency_score = psqi_result.get('sleep_latency_score', 0)
        sleep_duration_score = psqi_result.get('sleep_duration_score', 0)
        sleep_efficiency_score = psqi_result.get('sleep_efficiency_score', 0)
        sleep_disturbance_score = psqi_result.get('sleep_disturbance_score', 0)
        use_of_sleep_medication_score = psqi_result.get('use_of_sleep_medication_score', 0)
        daytime_dysfunction_score = psqi_result.get('daytime_dysfunction_score', 0)

        # 수면 세부 상태
        sleep_quality_status = psqi_result.get('sleep_quality_status', '')
        sleep_latency_status = psqi_result.get('sleep_latency_status', '')
        sleep_duration_status = psqi_result.get('sleep_duration_status', '')
        sleep_efficiency_status = psqi_result.get('sleep_efficiency_status', '')
        sleep_disturbance_status = psqi_result.get('sleep_disturbance_status', '')
        use_of_sleep_medication_status = psqi_result.get('use_of_sleep_medication_status', '')
        daytime_dysfunction_status = psqi_result.get('daytime_dysfunction_status', '')

        # 일반 건강 세부 점수
        cognition_score = whodas_result.get('cognition_score', 0)
        mobility_score = whodas_result.get('mobility_score', 0)
        self_care_score = whodas_result.get('self_care_score', 0)
        getting_along_score = whodas_result.get('getting_along_score', 0)
        life_activities_score = whodas_result.get('life_activities_score', 0)
        participation_score = whodas_result.get('participation_score', 0)

        # 일반 건강 세부 상태
        cognition_status = whodas_result.get('cognition_status', '')
        mobility_status = whodas_result.get('mobility_status', '')
        self_care_status = whodas_result.get('self_care_status', '')
        getting_along_status = whodas_result.get('getting_along_status', '')
        life_activities_status = whodas_result.get('life_activities_status', '')
        participation_status = whodas_result.get('participation_status', '')

        # 감정 세부 점수
        depression_score = dass_result.get('depression_score', 0)
        anxiety_score = dass_result.get('anxiety_score', 0)
        stress_score = dass_result.get('stress_score', 0)

        # 감정 세부 상태
        depression_status = dass_result.get('depression_status', '')
        anxiety_status = dass_result.get('anxiety_status', '')
        stress_status = dass_result.get('stress_status', '')

        # 외로움 세부 점수
        loneliness_score = lsis_result.get('loneliness_score', 0)
        social_support_score = lsis_result.get('social_support_score', 0)
        social_network_score = lsis_result.get('social_network_score', 0)

        # 외로움 세부 상태
        loneliness_status = lsis_result.get('loneliness_status', '')
        social_support_status = lsis_result.get('social_support_status', '')
        social_network_status = lsis_result.get('social_network_status', '')

        context = {
            'name': name,
            'psqi_k': psqi_k,
            'psqi_k_percent': psqi_k_percent,
            'psqi_k_status': psqi_k_status,
            'whodas_k': whodas_k,
            'whodas_k_percent': whodas_k_percent,
            'whodas_k_status': whodas_k_status,
            'dass': dass,
            'dass_percent': dass_percent,
            'dass_status': dass_status,
            'lsis': lsis,
            'lsis_percent': lsis_percent,
            'lsis_status': lsis_status,
            'report_overview_intro': ReportAPIView.load_description('contents/descriptions/report_overview_intro.txt'),
            'assessment_results_intro': ReportAPIView.load_description(
                'contents/descriptions/assessment_results_intro.txt',
                name=name),

            'assessment_results_summary': ReportAPIView.load_description(
                'contents/descriptions/assessment_results_summary.txt',
                psqi_k_status=psqi_k_status,
                whodas_k_status=whodas_k_status,
                dass_status=dass_status,
                lsis_status=lsis_status,
                assessment_results_summary_refined=assessment_results_summary_refined),

            'psqi_bar_description': ReportAPIView.load_description('contents/descriptions/psqi_bar_description.txt',
                                                                   score=psqi_k, score_status=psqi_k_status),
            'whodas_bar_description': ReportAPIView.load_description('contents/descriptions/whodas_bar_description.txt',
                                                                     score=whodas_k, score_status=whodas_k_status),
            'dass_bar_description': ReportAPIView.load_description('contents/descriptions/dass_bar_description.txt',
                                                                   score=dass, score_status=dass_status),
            'lsis_bar_description': ReportAPIView.load_description('contents/descriptions/lsis_bar_description.txt',
                                                                   score=lsis, score_status=lsis_status),
            'sleep_quality_intro': ReportAPIView.load_description('contents/descriptions/sleep_quality_intro.txt'),
            'physical_health_intro': ReportAPIView.load_description('contents/descriptions/physical_health_intro.txt'),
            'depression_intro': ReportAPIView.load_description('contents/descriptions/depression_intro.txt'),
            'loneliness_intro': ReportAPIView.load_description('contents/descriptions/loneliness_intro.txt'),

            'psqi_detail_range': list(range(3 + 1)),
            'whodas_detail_range': list(range(8 + 1)),
            'dass_detail_range': list(range(0, 42 + 1, 6)),
            'lsis_detail_range': list(range(6 + 1)),

            'psqi_detail_description': ReportAPIView.load_description(
                'contents/descriptions/psqi_detail_description.txt',
                score1=sleep_quality_score,
                status1=sleep_quality_status,
                score2=sleep_latency_score,
                status2=sleep_latency_status,
                score3=sleep_duration_score,
                status3=sleep_duration_status,
                score4=sleep_efficiency_score,
                status4=sleep_efficiency_status,
                score5=sleep_disturbance_score,
                status5=sleep_disturbance_status,
                score6=use_of_sleep_medication_score,
                status6=use_of_sleep_medication_status,
                score7=daytime_dysfunction_score,
                status7=daytime_dysfunction_status),

            'whodas_detail_description': ReportAPIView.load_description(
                'contents/descriptions/whodas_detail_description.txt',
                score1=cognition_score,
                status1=cognition_status,
                score2=mobility_score,
                status2=mobility_status,
                score3=self_care_score,
                status3=self_care_status,
                score4=getting_along_score,
                status4=getting_along_status,
                score5=life_activities_score,
                status5=life_activities_status,
                score6=participation_score,
                status6=participation_status),

            'dass_detail_description': ReportAPIView.load_description(
                'contents/descriptions/dass_detail_description.txt',
                score1=depression_score,
                status1=depression_status,
                score2=anxiety_score,
                status2=anxiety_status,
                score3=stress_score,
                status3=stress_status),

            'lsis_detail_description': ReportAPIView.load_description(
                'contents/descriptions/lsis_detail_description.txt',
                score1=loneliness_score,
                status1=loneliness_status,
                score2=social_support_score,
                status2=social_support_status,
                score3=social_network_score,
                status3=social_network_status),

            'feedback_recommendation_description': ReportAPIView.load_description(
                'contents/descriptions/feedback_recommendation_description.txt'),

            'sleep_quality_score': sleep_quality_score,
            'sleep_latency_score': sleep_latency_score,
            'sleep_duration_score': sleep_duration_score,
            'sleep_efficiency_score': sleep_efficiency_score,
            'sleep_disturbance_score': sleep_disturbance_score,
            'use_of_sleep_medication_score': use_of_sleep_medication_score,
            'daytime_dysfunction_score': daytime_dysfunction_score,

            'sleep_quality_status': sleep_quality_status,
            'sleep_latency_status': sleep_latency_status,
            'sleep_duration_status': sleep_duration_status,
            'sleep_efficiency_status': sleep_efficiency_status,
            'sleep_disturbance_status': sleep_disturbance_status,
            'use_of_sleep_medication_status': use_of_sleep_medication_status,
            'daytime_dysfunction_status': daytime_dysfunction_status,

            'cognition_score': cognition_score,
            'mobility_score': mobility_score,
            'self_care_score': self_care_score,
            'getting_along_score': getting_along_score,
            'life_activities_score': life_activities_score,
            'participation_score': participation_score,

            'cognition_status': cognition_status,
            'mobility_status': mobility_status,
            'self_care_status': self_care_status,
            'getting_along_status': getting_along_status,
            'life_activities_status': life_activities_status,
            'participation_status': participation_status,

            'depression_score': depression_score,
            'anxiety_score': anxiety_score,
            'stress_score': stress_score,

            'depression_status': depression_status,
            'anxiety_status': anxiety_status,
            'stress_status': stress_status,

            'loneliness_score': loneliness_score,
            'social_support_score': social_support_score,
            'social_network_score': social_network_score,

            'loneliness_status': loneliness_status,
            'social_support_status': social_support_status,
            'social_network_status': social_network_status,
        }

        context['sleep_components'] = [
            {
                "label": "주관적 수면의 질",
                "score": sleep_quality_score,
                "percent": round(sleep_quality_score / 3 * 100, 2),
                "rev_percent": 100 - round(sleep_quality_score / 3 * 100, 2),
                "status": sleep_quality_status
            },
            {
                "label": "수면 잠복기",
                "score": sleep_latency_score,
                "percent": round(sleep_latency_score / 3 * 100, 2),
                "rev_percent": 100 - round(sleep_latency_score / 3 * 100, 2),
                "status": sleep_latency_status
            },
            {
                "label": "수면 시간",
                "score": sleep_duration_score,
                "percent": round(sleep_duration_score / 3 * 100, 2),
                "rev_percent": 100 - round(sleep_duration_score / 3 * 100, 2),
                "status": sleep_duration_status,
            },
            {
                "label": "수면 효율",
                "score": sleep_efficiency_score,
                "percent": round(sleep_efficiency_score / 3 * 100, 2),
                "rev_percent": 100 - round(sleep_efficiency_score / 3 * 100, 2),
                "status": sleep_efficiency_status,
            },
            {
                "label": "수면 방해",
                "score": sleep_disturbance_score,
                "percent": round(sleep_disturbance_score / 3 * 100, 2),
                "rev_percent": 100 - round(sleep_disturbance_score / 3 * 100, 2),
                "status": sleep_disturbance_status,
            },
            {
                "label": "수면제 사용",
                "score": use_of_sleep_medication_score,
                "percent": round(use_of_sleep_medication_score / 3 * 100, 2),
                "rev_percent": 100 - round(use_of_sleep_medication_score / 3 * 100, 2),
                "status": use_of_sleep_medication_status,
            },
            {
                "label": "주간 기능장애",
                "score": daytime_dysfunction_score,
                "percent": round(daytime_dysfunction_score / 3 * 100, 2),
                "rev_percent": 100 - round(daytime_dysfunction_score / 3 * 100, 2),
                "status": daytime_dysfunction_status,
            },
        ]

        context['general_health_components'] = [
            {
                "label": "인지",
                "score": cognition_score,
                "status": cognition_status,
                "percent": round(cognition_score / 8 * 100, 2),
                "rev_percent": 100 - round(cognition_score / 8 * 100, 2),
            },
            {
                "label": "이동",
                "score": mobility_score,
                "status": mobility_status,
                "percent": round(mobility_score / 8 * 100, 2),
                "rev_percent": 100 - round(mobility_score / 8 * 100, 2),
            },
            {
                "label": "자가 돌봄",
                "score": self_care_score,
                "status": self_care_status,
                "percent": round(self_care_score / 8 * 100, 2),
                "rev_percent": 100 - round(self_care_score / 8 * 100, 2),
            },
            {
                "label": "개인 관계",
                "score": getting_along_score,
                "status": getting_along_status,
                "percent": round(getting_along_score / 8 * 100, 2),
                "rev_percent": 100 - round(getting_along_score / 8 * 100, 2),
            },
            {
                "label": "일상 생활 활동",
                "score": life_activities_score,
                "status": life_activities_status,
                "percent": round(life_activities_score / 8 * 100, 2),
                "rev_percent": 100 - round(life_activities_score / 8 * 100, 2),
            },
            {
                "label": "사회적 참여",
                "score": participation_score,
                "status": participation_status,
                "percent": round(participation_score / 8 * 100, 2),
                "rev_percent": 100 - round(participation_score / 8 * 100, 2),
            },
        ]

        context['emotion_components'] = [
            {
                "label": "우울",
                "score": depression_score,
                "status": depression_status,
                "percent": round(depression_score / 42 * 100, 2),
                "rev_percent": 100 - round(depression_score / 42 * 100, 2),
            },
            {
                "label": "불안",
                "score": anxiety_score,
                "status": anxiety_status,
                "percent": round(anxiety_score / 42 * 100, 2),
                "rev_percent": 100 - round(anxiety_score / 42 * 100, 2),
            },
            {
                "label": "스트레스",
                "score": stress_score,
                "status": stress_status,
                "percent": round(stress_score / 42 * 100, 2),
                "rev_percent": 100 - round(stress_score / 42 * 100, 2),
            },
        ]

        context['loneliness_components'] = [
            {
                "label": "외로움",
                "score": loneliness_score,
                "status": loneliness_status,
                "percent": round(loneliness_score / 6 * 100, 2),
                "rev_percent": 100 - round(loneliness_score / 6 * 100, 2),
            },
            {
                "label": "사회적 지지",
                "score": social_support_score,
                "status": social_support_status,
                "percent": round(social_support_score / 6 * 100, 2),
                "rev_percent": 100 - round(social_support_score / 6 * 100, 2),
            },
            {
                "label": "사회적 관계망",
                "score": social_network_score,
                "status": social_network_status,
                "percent": round(social_network_score / 6 * 100, 2),
                "rev_percent": 100 - round(social_network_score / 6 * 100, 2),
            },
        ]

        return context

    @staticmethod
    def build_report_context_from_id(user_id: int) -> dict:
        # 사용자 이름 불러오기
        basic_info = get_object_or_404(BasicInfo, id=user_id)
        name = basic_info.name

        # 가장 최근 설문 데이터 1개 가져오기
        psqi_latest_record = SleepHealth.objects.filter(participant_id=user_id).order_by('-id').first()
        whodas_latest_record = GeneralHealth.objects.filter(participant_id=user_id).order_by('-id').first()
        dass_latest_record = Emotion.objects.filter(participant_id=user_id).order_by('-id').first()
        lsis_latest_record = Loneliness.objects.filter(participant_id=user_id).order_by('-id').first()

        # 결과 평가
        psqi_result = SleepHealthBaseView.evaluate_sleep_health([psqi_latest_record])[0] if psqi_latest_record else {}
        whodas_result = GeneralHealthBaseView.evaluate_general_health([whodas_latest_record])[0] if whodas_latest_record else {}
        dass_result = EmotionBaseView.evaluate_emotion([dass_latest_record])[0] if dass_latest_record else {}
        lsis_result = LonelinessBaseView.evaluate_loneliness([lsis_latest_record])[0] if lsis_latest_record else {}

        return ReportAPIView._build_context_from_evaluated_results(psqi_result, whodas_result, dass_result, lsis_result, name)

    @staticmethod
    def build_report_context_from_data(validated_data: dict) -> dict:
        """
        WholeScoresWithPathSerializer 데이터 기반으로 context를 생성합니다.
        """
        # 제공된 데이터에서 각 설문 데이터 추출
        PSQI_data = validated_data.get('PSQI_data', {})
        WHODAS_data = validated_data.get('WHODAS_data', {})
        DASS21_data = validated_data.get('DASS21_data', {})
        LSIS_data = validated_data.get('LSIS_data', {})
        
        # 기본 이름 설정 (데이터에서 제공되지 않으면 기본값 사용)
        name = validated_data.get('name', '설문자')
        
        # 각 설문 데이터로 모델 인스턴스 생성
        psqi_instance = SleepHealth(**PSQI_data) if PSQI_data else None
        whodas_instance = GeneralHealth(**WHODAS_data) if WHODAS_data else None
        dass_instance = Emotion(**DASS21_data) if DASS21_data else None
        lsis_instance = Loneliness(**LSIS_data) if LSIS_data else None
        
        # 결과 평가
        psqi_result = SleepHealthBaseView.evaluate_sleep_health([psqi_instance])[0] if psqi_instance else {}
        whodas_result = GeneralHealthBaseView.evaluate_general_health([whodas_instance])[0] if whodas_instance else {}
        dass_result = EmotionBaseView.evaluate_emotion([dass_instance])[0] if dass_instance else {}
        lsis_result = LonelinessBaseView.evaluate_loneliness([lsis_instance])[0] if lsis_instance else {}
        
        return ReportAPIView._build_context_from_evaluated_results(psqi_result, whodas_result, dass_result, lsis_result, name)

    @staticmethod
    def generate_report_pdf_from_id(validated_data, context_option=False):
        """
        사용자 ID 기반으로 PDF 리포트를 생성 (playwright 기반).
        """
        user_id = validated_data.get('id')
        pdf_path = validated_data.get('pdf_path')
        file_name = validated_data.get('file_name')

        context = ReportAPIView.build_report_context_from_id(user_id)
        html_string = render_to_string('report_template.html', context)

        # static 경로 수동 치환
        static_root = settings.STATIC_ROOT.replace('\\', '/')
        html_string = html_string.replace('/static/', f'file:///{static_root}/')

        # 1. 저장 경로 설정
        os.makedirs(pdf_path, exist_ok=True)
        output_path = os.path.join(pdf_path, file_name)

        # 2. HTML 임시 파일 생성
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as tmp:
            tmp.write(html_string)
            tmp_html_path = tmp.name

        try:
            # 3. Playwright를 사용한 PDF 생성
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f'file:///{tmp_html_path}', wait_until='networkidle')
                page.pdf(path=output_path, format='A4', margin={'top': '20px', 'bottom': '20px'}, print_background=True)
                browser.close()
        finally:
            # 4. 임시 HTML 파일 정리
            try:
                os.remove(tmp_html_path)
            except OSError:
                # 파일이 이미 삭제되었거나 삭제할 수 없는 경우 무시
                pass

        if context_option:
            return context
        else:
            return None

    @staticmethod
    def generate_report_pdf_from_data(validated_data, context_option=False):
        """
        WholeScoresWithPathSerializer 데이터 기반으로 PDF 리포트를 생성 (playwright 기반).
        """
        # validated_data에서 필요한 정보 추출
        pdf_path = validated_data.get('pdf_path')
        file_name = validated_data.get('file_name')
        
        # context 생성 (새로운 메서드 필요)
        context = ReportAPIView.build_report_context_from_data(validated_data)
        html_string = render_to_string('report_template.html', context)

        # static 경로 수동 치환
        static_root = settings.STATIC_ROOT.replace('\\', '/')
        html_string = html_string.replace('/static/', f'file:///{static_root}/')

        # 1. 저장 경로 설정
        os.makedirs(pdf_path, exist_ok=True)
        output_path = os.path.join(pdf_path, file_name)

        # 2. HTML 임시 파일 생성
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as tmp:
            tmp.write(html_string)
            tmp_html_path = tmp.name

        try:
            # 3. Playwright를 사용한 PDF 생성
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f'file:///{tmp_html_path}', wait_until='networkidle')
                page.pdf(path=output_path, format='A4', margin={'top': '20px', 'bottom': '20px'}, print_background=True)
                browser.close()
        finally:
            # 4. 임시 HTML 파일 정리
            try:
                os.remove(tmp_html_path)
            except OSError:
                # 파일이 이미 삭제되었거나 삭제할 수 없는 경우 무시
                pass

        if context_option:
            return context
        else:
            return None