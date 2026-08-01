from django.db import models

from profiles.models import Profile
from utils.constants import DISTRICT_CHOICES


class Scenario(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='scenarios')
	scenario_type = models.CharField(
		max_length=20,
		choices=[
			('move_now', '지금 독립'),
			('wait_12m', '12개월 대기'),
			('lower_cost_region', '저비용 지역'),
			('high_deposit', '고보증금'),
		],
		default='move_now',
	)
	district = models.CharField(max_length=10, choices=DISTRICT_CHOICES)
	housing_type = models.CharField(max_length=10, choices=[('아파트', '아파트'), ('오피스텔', '오피스텔'), ('연립·다세대', '연립·다세대')])
	desired_area_m2 = models.FloatField(default=35.0)
	move_in_after_months = models.PositiveSmallIntegerField(default=0)
	deposit = models.PositiveIntegerField()
	monthly_rent = models.PositiveIntegerField(default=0)
	contract_months = models.PositiveSmallIntegerField(default=24)
	deposit_loan_amount = models.PositiveIntegerField(default=0)
	loan_interest_rate = models.FloatField(default=0.0)
	loan_repayment_type = models.CharField(
		max_length=20,
		choices=[('interest_only', '이자만 상환'), ('none', '대출 없음')],
		default='none',
	)
	moving_cost = models.PositiveIntegerField(default=0)
	brokerage_fee = models.PositiveIntegerField(default=0)
	monthly_support = models.PositiveIntegerField(default=0)
	support_months = models.PositiveSmallIntegerField(default=0)
	deposit_return_rate = models.FloatField(default=0.98)
	contract_type = models.CharField(
		max_length=20,
		choices=[('monthly_rent', '월세'), ('jeonse', '전세')],
		default='monthly_rent',
	)
	conversion_rate_annual = models.FloatField(default=0.05)
	contract_slider_pct = models.SmallIntegerField(default=30)
	created_at = models.DateTimeField(auto_now_add=True)


class Diagnosis(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    scenario_id_ai = models.CharField(max_length=50, blank=True, default='')
    achievement_score = models.PositiveSmallIntegerField(null=True, blank=True)
    suitability = models.CharField(max_length=10, blank=True, default='')
    goal_probability = models.FloatField()
    district = models.CharField(max_length=10)
    housing_type = models.CharField(max_length=10)
    raw_payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class TimingComparison(models.Model):
	"""Step4 화면 전용. 같은 조건에서 독립 시점(지금/1년후/2년후)만 다르게 비교한 결과.
	Diagnosis와 다른 모델이다 — 헷갈리지 말 것."""
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
	base_scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
	raw_payload = models.JSONField()
	created_at = models.DateTimeField(auto_now_add=True)
