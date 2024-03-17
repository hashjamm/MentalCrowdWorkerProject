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