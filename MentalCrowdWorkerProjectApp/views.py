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
    JobSatisfactionSerializer, JobSatisfactionStressFactorsSerializer, SleepHealthSerializer, GeneralHealthSerializer, \
    EmotionSerializer, LonelinessSerializer, PSQISerializer, WHODASSerializer, DASS21Serializer


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

            keys_to_extract = ['psqi_k', 'status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def evaluate_sleep_health(records):
        result_list = []
        for one_record in records:
            # Define scoring conditions
            c1 = one_record.result_6
            c2_element_1 = 3 if one_record.result_2 >= 61 else 2 if one_record.result_2 >= 31 else 1 if one_record.result_2 >= 16 else 0
            pre_c2 = c2_element_1 + one_record.result_5a
            c2 = 3 if pre_c2 >= 5 else 2 if pre_c2 >= 3 else 1 if pre_c2 >= 1 else 0

            if one_record.result_4 < 300:
                c3 = 3
            elif one_record.result_4 < 360:
                c3 = 2
            elif one_record.result_4 < 420:
                c3 = 1
            else:
                c3 = 0

            arbitrary_day = datetime.datetime.today().date()
            datetime_result_3 = datetime.datetime.combine(arbitrary_day, one_record.result_3)
            datetime_result_1 = datetime.datetime.combine(arbitrary_day, one_record.result_1)
            pre_c4 = (one_record.result_4 / ((datetime_result_3 - datetime_result_1).total_seconds() / 60)) * 100
            c4 = 3 if pre_c4 < 65 else 2 if pre_c4 < 75 else 1 if pre_c4 < 85 else 0

            pre_c5 = sum([one_record.result_5b, one_record.result_5c, one_record.result_5d, one_record.result_5e,
                          one_record.result_5f, one_record.result_5g, one_record.result_5h, one_record.result_5i,
                          one_record.result_5j])
            c5 = 3 if pre_c5 > 18 else 2 if pre_c5 > 9 else 1 if pre_c5 > 0 else 0

            c6 = one_record.result_7
            pre_c7 = one_record.result_8 + one_record.result_9
            c7 = 3 if pre_c7 > 5 else 2 if pre_c7 > 3 else 1 if pre_c7 > 1 else 0

            psqi_k = sum([c1, c2, c3, c4, c5, c6, c7])
            status = "disordered" if psqi_k > 10 else "disturbed" if psqi_k > 4 else "normal"

            record_dict = model_to_dict(one_record)
            record_dict['psqi_k'] = psqi_k
            record_dict['status'] = status
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

            keys_to_extract = ['raw_whodas_k', 'standardized_whodas_k', 'status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def evaluate_general_health(records):
        result_list = []
        for one_record in records:
            # Define scoring conditions
            # c1: 인지, c2: 이동성, c3: 자기 관리, c4: 대인 관계, c5: 생활 활동, c6: 사회 참여
            c1 = (one_record.result_1 + one_record.result_2) / 2
            c2 = (one_record.result_3 + one_record.result_4) / 2
            c3 = (one_record.result_5 + one_record.result_6) / 2
            c4 = (one_record.result_7 + one_record.result_8) / 2
            c5 = (one_record.result_9 + one_record.result_10) / 2
            c6 = (one_record.result_11 + one_record.result_12) / 2

            raw_whodas_k = c1 + c2 + c3 + c4 + c5 + c6
            standardized_whodas_k = round(100 * (raw_whodas_k - 6) / (30 - 6), 2)

            if 0 <= standardized_whodas_k < 5:
                status = "None"
            elif 5 <= standardized_whodas_k < 25:
                status = "Mild"
            elif 25 <= standardized_whodas_k < 50:
                status = "Moderate"
            elif 50 <= standardized_whodas_k < 96:
                status = "Severe"
            else:
                status = "Extreme"

            record_dict = model_to_dict(one_record)
            record_dict['raw_whodas_k'] = raw_whodas_k
            record_dict['standardized_whodas_k'] = standardized_whodas_k
            record_dict['status'] = status
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

            keys_to_extract = ['depression_scale', 'depression_status', 'anxiety_scale', 'anxiety_status',
                               'stress_scale', 'stress_status']

            sub_dict = {key: result[0][key] for key in keys_to_extract if key in result[0]}

            return Response(sub_dict, status=status.HTTP_200_OK)

        else:
            print(serialized_data.errors)

            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def evaluate_emotion(records):
        result_list = []
        for one_record in records:
            # Define scoring conditions
            # c1: Depression Scale, c2: Anxiety Scale, c3: Stress Scale
            c1_list = [one_record.result_3, one_record.result_5, one_record.result_10, one_record.result_13,
                       one_record.result_16, one_record.result_17, one_record.result_21]
            c2_list = [one_record.result_2, one_record.result_4, one_record.result_7, one_record.result_9,
                       one_record.result_15, one_record.result_19, one_record.result_20]
            c3_list = [one_record.result_1, one_record.result_6, one_record.result_8, one_record.result_11,
                       one_record.result_12, one_record.result_14, one_record.result_18]

            c1 = sum(c1_list) - len(c1_list)
            c2 = sum(c2_list) - len(c2_list)
            c3 = sum(c3_list) - len(c3_list)

            if 0 <= c1 < 5:
                c1_status = "Normal"
            elif 5 <= c1 < 7:
                c1_status = "Mild"
            elif 7 <= c1 < 11:
                c1_status = "Moderate"
            elif 11 <= c1 < 14:
                c1_status = "Severe"
            else:
                c1_status = "Extreme"

            if 0 <= c2 < 4:
                c2_status = "Normal"
            elif 4 <= c2 < 6:
                c2_status = "Mild"
            elif 6 <= c2 < 8:
                c2_status = "Moderate"
            elif 8 <= c2 < 10:
                c2_status = "Severe"
            else:
                c2_status = "Extreme"

            if 0 <= c3 < 8:
                c3_status = "Normal"
            elif 8 <= c3 < 10:
                c3_status = "Mild"
            elif 10 <= c3 < 13:
                c3_status = "Moderate"
            elif 13 <= c3 < 17:
                c3_status = "Severe"
            else:
                c3_status = "Extreme"

            record_dict = model_to_dict(one_record)
            record_dict['depression_scale'] = c1
            record_dict['depression_status'] = c1_status
            record_dict['anxiety_scale'] = c2
            record_dict['anxiety_status'] = c2_status
            record_dict['stress_scale'] = c3
            record_dict['stress_status'] = c3_status
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
    def get_whole_loneliness(self, request):

        queryset = Loneliness.objects.all()

        try:

            serializer = LonelinessSerializer(queryset, many=True)

            return Response(serializer.data)

        except Loneliness.DoesNotExist:

            raise NotFound("Emotion 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def get_personal_loneliness(self, request, user_id):

        try:

            basic_info = BasicInfo.objects.get(id=user_id)
            queryset = basic_info.loneliness_set.all()

            serialized_data = LonelinessSerializer(queryset, many=True).data

            return Response(serialized_data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except Loneliness.DoesNotExist:

            raise NotFound("Loneliness 데이터가 존재하지 않습니다.")
