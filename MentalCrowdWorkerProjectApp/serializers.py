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