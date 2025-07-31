# Create your models here.
from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator


class BasicInfo(models.Model):
    id = models.BigAutoField(help_text="BasicInfo pk", primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="사용자 이름")
    sex = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="성별")
    age = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="연령")
    edu_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="최종 학력")
    edu_level_etc = models.TextField(blank=True, null=True, verbose_name="기타 최종 학력 입력 내용")
    marital_status = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)], verbose_name="결혼 상태")
    income_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)],
                                       verbose_name="사회 경제 상태")
    career_duration = models.FloatField(validators=[MinValueValidator(0)], verbose_name="경력 기간")
    task_type = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)], verbose_name="업무 내용")
    task_description = models.TextField(verbose_name="업무 내용 입력 문자열", null=True)
    occupation_type = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], verbose_name="직업 형태")
    interest = models.TextField(verbose_name="주요 관심 입력 문자열", null=True)


class StressFactors(models.Model):
    id = models.BigAutoField(help_text="StressFactors pk", primary_key=True)
    type = models.CharField(max_length=50, unique=True)


class JobSatisfaction(models.Model):
    id = models.BigAutoField(help_text="JobSatisfaction pk", primary_key=True)
    participant_id = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name="BasicInfo pk",
                                       related_name='job_satisfaction_set')
    satisfaction_level = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                           verbose_name="업무 만족도")
    stress_factors = models.ManyToManyField(StressFactors, through="JobSatisfactionStressFactors")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
        # ManyToMany 필드는 save() 이후 별도로 처리해야 합니다.
        # 예: self.stress_factors.set([...])


class JobSatisfactionStressFactors(models.Model):
    id = models.BigAutoField(help_text="JobSatisfactionStressFactors pk", primary_key=True)
    job_satisfaction = models.ForeignKey(JobSatisfaction, on_delete=models.CASCADE,
                                         related_name='job_satisfaction_stress_factors_set')
    stress_factors = models.ForeignKey(StressFactors, on_delete=models.DO_NOTHING,
                                       related_name="job_satisfaction_stress_factors_set")
    input_text = models.TextField(verbose_name="입력 문자열", null=True)


class SleepHealth(models.Model):
    id = models.BigAutoField(help_text="SleepHealth pk", primary_key=True)
    participant_id = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name="BasicInfo pk",
                                       related_name='sleep_health_set')
    result_1 = models.TimeField(verbose_name="수면 시작 시각")
    result_2 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)],
                                   verbose_name="수면 까지 걸리는 시간(분)")
    result_3 = models.TimeField(verbose_name="평소 기상 시각")
    result_4 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1440)],
                                   verbose_name="실제 수면을 취한 시간(분)")
    result_5a = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-a")
    result_5b = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-b")
    result_5c = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-c")
    result_5d = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-d")
    result_5e = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-e")
    result_5f = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-f")
    result_5g = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-g")
    result_5h = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-h")
    result_5i = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항-i")
    result_5j = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], null=True,
                                    verbose_name="5번 문항-j")
    result_5j_input_text = models.TextField(verbose_name="입력된 기타 수면 장애 이유", null=True)
    result_6 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="6번 문항")
    result_7 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="7번 문항")
    result_8 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="8번 문항")
    result_9 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="9번 문항")


class GeneralHealth(models.Model):
    id = models.BigAutoField(help_text="GeneralHealth pk", primary_key=True)
    participant_id = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name="BasicInfo pk",
                                       related_name='general_health_set')
    result_1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="1번 문항")
    result_2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="2번 문항")
    result_3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="3번 문항")
    result_4 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="4번 문항")
    result_5 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="5번 문항")
    result_6 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="6번 문항")
    result_7 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="7번 문항")
    result_8 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="8번 문항")
    result_9 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="9번 문항")
    result_10 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="10번 문항")
    result_11 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="11번 문항")
    result_12 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="12번 문항")
    result_13 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], verbose_name="13번 문항")
    result_14 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], verbose_name="14번 문항")
    result_15 = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(30)], verbose_name="15번 문항")


class Emotion(models.Model):
    id = models.BigAutoField(help_text="Emotion pk", primary_key=True)
    participant_id = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name="BasicInfo pk",
                                       related_name='emotion_set')
    result_1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="1번 문항")
    result_2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="2번 문항")
    result_3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="3번 문항")
    result_4 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="4번 문항")
    result_5 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항")
    result_6 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="6번 문항")
    result_7 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="7번 문항")
    result_8 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="8번 문항")
    result_9 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="9번 문항")
    result_10 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="10번 문항")
    result_11 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="11번 문항")
    result_12 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="12번 문항")
    result_13 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="13번 문항")
    result_14 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="14번 문항")
    result_15 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="15번 문항")
    result_16 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="16번 문항")
    result_17 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="17번 문항")
    result_18 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="18번 문항")
    result_19 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="19번 문항")
    result_20 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="20번 문항")
    result_21 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="21번 문항")


class Loneliness(models.Model):
    id = models.BigAutoField(help_text="Loneliness pk", primary_key=True)
    participant_id = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name="BasicInfo pk",
                                       related_name='loneliness_set')
    result_1 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="1번 문항")
    result_2 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="2번 문항")
    result_3 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="3번 문항")
    result_4 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="4번 문항")
    result_5 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="5번 문항")
    result_6 = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)], verbose_name="6번 문항")
