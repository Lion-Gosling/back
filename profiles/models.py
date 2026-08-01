from django.db import models


class Profile(models.Model):
    age = models.PositiveSmallIntegerField()
    monthly_income = models.PositiveIntegerField()  # 원
    current_cash = models.PositiveIntegerField()  # 원
    monthly_living_cost = models.PositiveIntegerField()  # 원
    debt_balance = models.PositiveIntegerField(default=0)  # 원
    debt_monthly_payment = models.PositiveIntegerField(default=0)  # 원
    target_asset = models.PositiveIntegerField()  # 원
    target_months = models.PositiveSmallIntegerField(default=36)
    current_monthly_housing_cost = models.PositiveIntegerField(default=0)  # 원, 이사 전 현재 주거비
    current_housing_type = models.CharField(
        max_length=20,
        choices=[("family", "가족과 거주"), ("monthly_rent", "월세"), ("jeonse", "전세")],
        default="family",
    )
    is_target_asset_default = models.BooleanField(default=False)
    is_target_months_default = models.BooleanField(default=False)
    is_living_cost_default = models.BooleanField(default=False)
    existing_loan_interest_rate = models.FloatField(default=0.0)
    existing_loan_remaining_months = models.PositiveSmallIntegerField(default=0)
    existing_loan_repayment_type = models.CharField(
        max_length=20,
        choices=[("amortizing", "원리금균등"), ("interest_only", "이자만 상환"), ("none", "대출 없음")],
        default="none",
    )
    event_answers = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']