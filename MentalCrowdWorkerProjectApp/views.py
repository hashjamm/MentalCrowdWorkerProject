import datetime

from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from MentalCrowdWorkerProjectApp.models import BasicInfo, StressFactors, JobSatisfaction, JobSatisfactionStressFactors, \
    SleepHealth, GeneralHealth, Emotion, Loneliness
from MentalCrowdWorkerProjectApp.serializers import BasicInfoSerializer, StressFactorsSerializer, \
    JobSatisfactionSerializer, JobSatisfactionStressFactorsSerializer, PSQISerializer, WHODASSerializer, \
    DASS21Serializer, LSISSerializer, WholeScoresSerializer


# Create your views here.
class BasicInfoAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_basic_info(request)
        else:
            return self.get_personal_basic_info(request, user_id)

    @csrf_exempt
    def get_whole_basic_info(self, request):

        queryset = BasicInfo.objects.all()

        try:

            serializer = BasicInfoSerializer(queryset, many=True)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

    @csrf_exempt
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

    @csrf_exempt
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_job_satisfaction(request)
        else:
            return self.get_personal_job_satisfaction(request, user_id)

    @csrf_exempt
    def get_whole_job_satisfaction(self, request):

        queryset = JobSatisfaction.objects.all()

        try:

            serializer = JobSatisfactionSerializer(queryset, many=True)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("JobSatisfaction 데이터가 존재하지 않습니다.")

    @csrf_exempt
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_job_satisfaction_stress_factors(request)
        else:
            return self.get_personal_job_satisfaction_stress_factors(request, user_id)

    @csrf_exempt
    def get_whole_job_satisfaction_stress_factors(self, request):

        queryset = JobSatisfactionStressFactors.objects.all()

        try:

            serializer = JobSatisfactionStressFactorsSerializer(queryset, many=True)

            return Response(serializer.data)

        except JobSatisfactionStressFactors.DoesNotExist:

            raise NotFound("JobSatisfactionStressFactors 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def get_personal_job_satisfaction_stress_factors(self, request, user_id):

        try:

            basic_info = BasicInfo.objects.get(id=user_id)
            result = []

            for job_satisfaction in basic_info.job_satisfaction_set.all():
                job_satisfaction_stress_factors = job_satisfaction.job_satisfaction_stress_factors_set.all()
                serialized_data = JobSatisfactionStressFactorsSerializer(job_satisfaction_stress_factors,
                                                                         many=True).data

                result.append(serialized_data)

            return Response(result)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except JobSatisfaction.DoesNotExist:

            raise NotFound("JobSatisfaction 데이터가 존재하지 않습니다.")

        except JobSatisfactionStressFactors.DoesNotExist:

            raise NotFound("JobSatisfactionStressFactors 데이터가 존재하지 않습니다.")


class SleepHealthAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_sleep_health(request)
        else:
            return self.get_personal_sleep_health(request, user_id)

    @csrf_exempt
    def post(self, request):

        serialized_data = PSQISerializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = SleepHealth(**serialized_data.validated_data)
            input_data = [instance]
            result = SleepHealthAPIView.evaluate_sleep_health(input_data)

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

            psqi_k_status = "수면 장애" if psqi_k > 10 else "수면은 하고있으나 숙면을 취하지 못하는 상태" if psqi_k > 4 else "숙면"

            # 주희쌤께서 전달 주신 각 세부 항목별 점수에 대한 상태 기준에 따름. 공인된 것인지는 모르겠음
            sleep_quality_status = "나쁨" if c1 >= 2 else "좋음"
            sleep_latency_status = "길다" if c2 == 3 else "조금 길다" if c2 == 2 else "무난"
            sleep_duration_status = "짧음" if c3 == 3 else "적당" if c3 >= 1 else "충분"
            sleep_efficiency_status = "나쁨" if c4 == 3 else "중간" if c3 == 2 else "좋음"
            sleep_disturbance_status = "매우 있음" if c5 == 3 else "있음" if c5 == 2 else "없음"
            use_of_sleep_medication_status = "주당 3회 이상" if c6 == 3 else "주당 2회" if c6 == 2 else "주당 1회" if c6 == 1 else "없음"
            daytime_dysfunction_status = "문제 있음" if c7 >= 2 else "문제 없음"

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

    @csrf_exempt
    def get_whole_sleep_health(self, request):

        try:

            queryset = SleepHealth.objects.all()
            result_list = SleepHealthAPIView.evaluate_sleep_health(queryset)
            return Response(result_list)

        except SleepHealth.DoesNotExist:

            raise NotFound("SleepHealth 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def get_personal_sleep_health(self, request, user_id):

        try:

            basic_info = BasicInfo.objects.get(id=user_id)
            queryset = basic_info.sleep_health_set.all()
            result_list = SleepHealthAPIView.evaluate_sleep_health(queryset)
            return Response(result_list)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except SleepHealth.DoesNotExist:

            raise NotFound("SleepHealth 데이터가 존재하지 않습니다.")


class GeneralHealthAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_general_health(request)
        else:
            return self.get_personal_general_health(request, user_id)

    @csrf_exempt
    def post(self, request):

        serialized_data = WHODASSerializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = GeneralHealth(**serialized_data.validated_data)
            input_data = [instance]
            result = GeneralHealthAPIView.evaluate_general_health(input_data)

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

            whodas_k_status = "건강기능 매우 양호" if whodas_k < 18 \
                else "건강기능 주의" if whodas_k < 31 \
                else "건강기능 어려움" if whodas_k < 43 \
                else "건강기능 장애" if whodas_k < 61 \
                else "건강기능 심각한 장애"

            # 주희쌤께서 전달 주신 각 세부 항목별 점수에 대한 상태 기준에 따름. 공인된 것인지는 모르겠음
            cognition_status = "None" if c1 < 2 else "Mild" if c1 < 4 else "Moderate" if c1 < 6 else "Severe"
            mobility_status = "None" if c2 < 2 else "Mild" if c2 < 4 else "Moderate" if c2 < 6 else "Severe"
            self_care_status = "None" if c3 < 2 else "Mild" if c3 < 4 else "Moderate" if c3 < 6 else "Severe"
            getting_along_status = "None" if c4 < 2 else "Mild" if c4 < 4 else "Moderate" if c4 < 6 else "Severe"
            life_activities_status = "None" if c5 < 2 else "Mild" if c5 < 4 else "Moderate" if c5 < 6 else "Severe"
            participation_status = "None" if c6 < 2 else "Mild" if c6 < 4 else "Moderate" if c6 < 6 else "Severe"

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

    @csrf_exempt
    def get_whole_general_health(self, request):

        try:

            queryset = GeneralHealth.objects.all()
            result_list = GeneralHealthAPIView.evaluate_general_health(queryset)
            return Response(result_list)

        except GeneralHealth.DoesNotExist:

            raise NotFound("GeneralHealth 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def get_personal_general_health(self, request, user_id):

        try:

            basic_info = BasicInfo.objects.get(id=user_id)
            queryset = basic_info.general_health_set.all()
            result_list = GeneralHealthAPIView.evaluate_general_health(queryset)
            return Response(result_list)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except GeneralHealth.DoesNotExist:

            raise NotFound("GeneralHealth 데이터가 존재하지 않습니다.")


class EmotionAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_emotion(request)
        else:
            return self.get_personal_emotion(request, user_id)

    @csrf_exempt
    def post(self, request):

        serialized_data = DASS21Serializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = Emotion(**serialized_data.validated_data)
            input_data = [instance]
            result = EmotionAPIView.evaluate_emotion(input_data)

            keys_to_extract = ['depression_score', 'depression_status',
                               'anxiety_score', 'anxiety_status',
                               'stress_score', 'stress_status',
                               'dass', 'dass_status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

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

            depression_status = "정상" if c1 < 10 else "경증 우울 상태" if c1 < 14 else "보통의 우울 상태" if c1 < 21 \
                else "극심한 우울 상태" if c1 < 28 else "매우 심한 우울 상태"
            anxiety_status = "정상" if c2 < 8 else "경증 불안 상태" if c2 < 10 else "보통의 불안 상태" if c2 < 15 \
                else "극심한 불안 상태" if c2 < 20 else "매우 심한 불안 상태"
            stress_status = "정상" if c3 < 15 else "경증 스트레스" if c3 < 19 else "보통의 스트레스" if c3 < 26 \
                else "극심한 스트레스" if c3 < 34 else "매우 심한 스트레스"

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

    @csrf_exempt
    def get_whole_emotion(self, request):

        try:

            queryset = Emotion.objects.all()
            result_list = EmotionAPIView.evaluate_emotion(queryset)
            return Response(result_list)

        except Emotion.DoesNotExist:

            raise NotFound("Emotion 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def get_personal_emotion(self, request, user_id):

        try:

            basic_info = BasicInfo.objects.get(id=user_id)
            queryset = basic_info.emotion_set.all()
            result_list = EmotionAPIView.evaluate_emotion(queryset)
            return Response(result_list)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except Emotion.DoesNotExist:

            raise NotFound("Emotion 데이터가 존재하지 않습니다.")


class LonelinessAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        user_id = request.GET.get('id')

        if user_id is None:
            return self.get_whole_loneliness(request)
        else:
            return self.get_personal_loneliness(request, user_id)

    @csrf_exempt
    def post(self, request):

        serialized_data = LSISSerializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            instance = Loneliness(**serialized_data.validated_data)
            input_data = [instance]
            result = LonelinessAPIView.evaluate_loneliness(input_data)

            keys_to_extract = ['loneliness_score', 'loneliness_status',
                               'social_support_score', 'social_support_status',
                               'social_network_score', 'social_network_status',
                               'lsis', 'lsis_status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

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
            lsis_status = "사회적 관계 및 외로움 고위험군" if lsis >= 9 else "사회적 관계가 건강한 상태"

            loneliness_status = "고위험군" if c1 >= 3 else "정상"
            social_support_status = "고위험군" if c2 >= 4 else "정상"
            social_network_status = "고위험군" if c3 >= 4 else "정상"

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

    @csrf_exempt
    def get_whole_loneliness(self, request):

        try:

            queryset = Loneliness.objects.all()
            result_list = LonelinessAPIView.evaluate_loneliness(queryset)
            return Response(result_list)

        except Loneliness.DoesNotExist:

            raise NotFound("Emotion 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def get_personal_loneliness(self, request, user_id):

        try:

            basic_info = BasicInfo.objects.get(id=user_id)
            queryset = basic_info.loneliness_set.all()
            result_list = LonelinessAPIView.evaluate_loneliness(queryset)
            return Response(result_list)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except Loneliness.DoesNotExist:

            raise NotFound("Loneliness 데이터가 존재하지 않습니다.")


class WholeSurveysAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request):

        serialized_data = WholeScoresSerializer(data=request.data)

        if serialized_data.is_valid():

            # instance = serialized_data.create(serialized_data.validated_data)

            validated_data = serialized_data.validated_data

            # 각 스코어 계산에 필요한 데이터에 접근
            PSQI_data = validated_data.get('PSQI_data')
            WHODAS_data = validated_data.get('WHODAS_data')
            DASS21_data = validated_data.get('DASS21_data')
            LSIS_data = validated_data.get('LSIS_data')

            instance = SleepHealth(**PSQI_data)
            input_data = [instance]
            result = SleepHealthAPIView.evaluate_sleep_health(input_data)

            keys_to_extract = ['sleep_quality_score', 'sleep_quality_status',
                               'sleep_latency_score', 'sleep_latency_status',
                               'sleep_duration_score', 'sleep_duration_status',
                               'sleep_efficiency_score', 'sleep_efficiency_status',
                               'sleep_disturbance_score', 'sleep_disturbance_status',
                               'use_of_sleep_medication_score', 'use_of_sleep_medication_status',
                               'daytime_dysfunction_score', 'daytime_dysfunction_status',
                               'psqi_k', 'psqi_k_status']

            sub_dict1 = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            instance = GeneralHealth(**WHODAS_data)
            input_data = [instance]
            result = GeneralHealthAPIView.evaluate_general_health(input_data)

            keys_to_extract = ['cognition_score', 'cognition_status',
                               'mobility_score', 'mobility_status',
                               'self_care_score', 'self_care_status',
                               'getting_along_score', 'getting_along_status',
                               'life_activities_score', 'life_activities_status',
                               'participation_score', 'participation_status',
                               'whodas_k', 'whodas_k_status']

            sub_dict2 = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            instance = Emotion(**DASS21_data)
            input_data = [instance]
            result = EmotionAPIView.evaluate_emotion(input_data)

            keys_to_extract = ['depression_score', 'depression_status',
                               'anxiety_score', 'anxiety_status',
                               'stress_score', 'stress_status',
                               'dass', 'dass_status']

            sub_dict3 = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            instance = Loneliness(**LSIS_data)
            input_data = [instance]
            result = LonelinessAPIView.evaluate_loneliness(input_data)

            keys_to_extract = ['loneliness_score', 'loneliness_status',
                               'social_support_score', 'social_support_status',
                               'social_network_score', 'social_network_status',
                               'lsis', 'lsis_status']

            sub_dict4 = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            merged_dict = sub_dict1 | sub_dict2 | sub_dict3 | sub_dict4

            return Response(merged_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
