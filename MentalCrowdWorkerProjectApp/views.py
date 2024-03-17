from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from MentalCrowdWorkerProjectApp.models import BasicInfo, StressFactors, JobSatisfaction, JobSatisfactionStressFactors, \
    SleepHealth, GeneralHealth, Emotion, Loneliness
from MentalCrowdWorkerProjectApp.serializers import BasicInfoSerializer, StressFactorsSerializer, \
    JobSatisfactionSerializer, JobSatisfactionStressFactorsSerializer, SleepHealthSerializer, GeneralHealthSerializer, \
    EmotionSerializer, LonelinessSerializer


# Create your views here.
class BasicInfoAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @csrf_exempt
    def get(self, request):

        queryset = BasicInfo.objects.all()

        try:

            serializer = BasicInfoSerializer(queryset, many=True)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def post(self, request, id):

        queryset = BasicInfo.objects.get(id=id)

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

    @csrf_exempt
    def get(self, request):

        queryset = JobSatisfaction.objects.all()

        try:

            serializer = JobSatisfactionSerializer(queryset, many=True)

            return Response(serializer.data)

        except BasicInfo.DoesNotExist:

            raise NotFound("JobSatisfaction 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def post(self, request, id):

        try:

            basic_info = BasicInfo.objects.get(id=id)
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

    @csrf_exempt
    def get(self, request):

        queryset = JobSatisfactionStressFactors.objects.all()

        try:

            serializer = JobSatisfactionStressFactorsSerializer(queryset, many=True)

            return Response(serializer.data)

        except JobSatisfactionStressFactors.DoesNotExist:

            raise NotFound("JobSatisfactionStressFactors 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def post(self, request, id):

        try:

            basic_info = BasicInfo.objects.get(id=id)
            result = []
            
            for job_satisfaction in basic_info.job_satisfaction_set.all():

                job_satisfaction_stress_factors = job_satisfaction.job_satisfaction_stress_factors_set.all()
                serialized_data = JobSatisfactionStressFactorsSerializer(job_satisfaction_stress_factors, many=True).data
                
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

    @csrf_exempt
    def get(self, request):

        queryset = SleepHealth.objects.all()

        try:

            serializer = SleepHealthSerializer(queryset, many=True)

            return Response(serializer.data)

        except SleepHealth.DoesNotExist:

            raise NotFound("SleepHealth 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def post(self, request, id):

        try:

            basic_info = BasicInfo.objects.get(id=id)
            queryset = basic_info.sleep_health_set.all()

            serialized_data = SleepHealthSerializer(queryset, many=True).data

            return Response(serialized_data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except SleepHealth.DoesNotExist:

            raise NotFound("SleepHealth 데이터가 존재하지 않습니다.")


class GeneralHealthAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @csrf_exempt
    def get(self, request):

        queryset = GeneralHealth.objects.all()

        try:

            serializer = GeneralHealthSerializer(queryset, many=True)

            return Response(serializer.data)

        except GeneralHealth.DoesNotExist:

            raise NotFound("GeneralHealth 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def post(self, request, id):

        try:

            basic_info = BasicInfo.objects.get(id=id)
            queryset = basic_info.general_health_set.all()

            serialized_data = GeneralHealthSerializer(queryset, many=True).data

            return Response(serialized_data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except GeneralHealth.DoesNotExist:

            raise NotFound("GeneralHealth 데이터가 존재하지 않습니다.")


class EmotionAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @csrf_exempt
    def get(self, request):

        queryset = Emotion.objects.all()

        try:

            serializer = EmotionSerializer(queryset, many=True)

            return Response(serializer.data)

        except Emotion.DoesNotExist:

            raise NotFound("Emotion 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def post(self, request, id):

        try:

            basic_info = BasicInfo.objects.get(id=id)
            queryset = basic_info.emotion_set.all()

            serialized_data = EmotionSerializer(queryset, many=True).data

            return Response(serialized_data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except Emotion.DoesNotExist:

            raise NotFound("Emotion 데이터가 존재하지 않습니다.")


class LonelinessAPIView(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @csrf_exempt
    def get(self, request):

        queryset = Loneliness.objects.all()

        try:

            serializer = LonelinessSerializer(queryset, many=True)

            return Response(serializer.data)

        except Loneliness.DoesNotExist:

            raise NotFound("Emotion 데이터가 존재하지 않습니다.")

    @csrf_exempt
    def post(self, request, id):

        try:

            basic_info = BasicInfo.objects.get(id=id)
            queryset = basic_info.loneliness_set.all()

            serialized_data = LonelinessSerializer(queryset, many=True).data

            return Response(serialized_data)

        except BasicInfo.DoesNotExist:

            raise NotFound("BasicInfo 데이터가 존재하지 않습니다.")

        except Loneliness.DoesNotExist:

            raise NotFound("Loneliness 데이터가 존재하지 않습니다.")