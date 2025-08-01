from rest_framework import serializers

from MentalCrowdWorkerProjectApp.models import BasicInfo, JobSatisfaction, JobSatisfactionStressFactors, StressFactors, \
    SleepHealth, GeneralHealth, Emotion, Loneliness


class BasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = '__all__'


class JobSatisfactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSatisfaction
        fields = '__all__'


class JobSatisfactionStressFactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSatisfactionStressFactors
        fields = '__all__'


class StressFactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StressFactors
        fields = '__all__'


class SleepHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepHealth
        fields = '__all__'


class GeneralHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralHealth
        fields = '__all__'


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = '__all__'


class LonelinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loneliness
        fields = '__all__'


class PSQISerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepHealth
        fields = ['result_1', 'result_2', 'result_3', 'result_4', 'result_5a', 'result_5b', 'result_5c', 'result_5d',
                  'result_5e', 'result_5f', 'result_5g', 'result_5h', 'result_5i', 'result_5j', 'result_5j_input_text',
                  'result_6', 'result_7', 'result_8', 'result_9']


class WHODASSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralHealth
        fields = ['result_1', 'result_2', 'result_3', 'result_4', 'result_5', 'result_6', 'result_7', 'result_8',
                  'result_9', 'result_10', 'result_11', 'result_12', 'result_13', 'result_14', 'result_15']


class DASS21Serializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['result_1', 'result_2', 'result_3', 'result_4', 'result_5', 'result_6', 'result_7', 'result_8',
                  'result_9', 'result_10', 'result_11', 'result_12', 'result_13', 'result_14', 'result_15', 'result_16',
                  'result_17', 'result_18', 'result_19', 'result_20', 'result_21']


class LSISSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loneliness
        fields = ['result_1', 'result_2', 'result_3', 'result_4', 'result_5', 'result_6']


class WholeScoresSerializer(serializers.Serializer):
    PSQI_data = PSQISerializer()
    WHODAS_data = WHODASSerializer()
    DASS21_data = DASS21Serializer()
    LSIS_data = LSISSerializer()


class WholeScoresWithPathSerializer(serializers.Serializer):
    PSQI_data = PSQISerializer()
    WHODAS_data = WHODASSerializer()
    DASS21_data = DASS21Serializer()
    LSIS_data = LSISSerializer()
    pdf_path = serializers.CharField()
    file_name = serializers.CharField()


class ReportRequestSerializer(serializers.Serializer):
    """
    리포트 생성 요청을 위한 serializer입니다.
    id만으로 DB에서 데이터를 조회하여 리포트를 생성하는 경우에 사용됩니다.
    """
    id = serializers.IntegerField(help_text="사용자 ID")
    pdf_path = serializers.CharField(help_text="PDF 저장 경로")
    file_name = serializers.CharField(help_text="PDF 파일명")
