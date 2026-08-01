from django.db import models

from utils.constants import DISTRICT_CHOICES


class RegionPriceStat(models.Model):
    district = models.CharField(max_length=10, choices=DISTRICT_CHOICES)
    housing_type = models.CharField(
        max_length=10,
        choices=[('아파트', '아파트'), ('오피스텔', '오피스텔'), ('연립·다세대', '연립·다세대')]
    )
    eq_rent = models.PositiveIntegerField()
    conversion_rate_annual = models.FloatField()
    min_deposit_floor = models.PositiveIntegerField()
    default_slider_pct = models.SmallIntegerField()
    moving_cost_avg = models.PositiveIntegerField()
    brokerage_fee_avg = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('district', 'housing_type')


class AgeIncomeBenchmark(models.Model):
    age_min = models.PositiveSmallIntegerField()
    age_max = models.PositiveSmallIntegerField()
    target_asset_default = models.PositiveIntegerField()
    target_months_default = models.PositiveSmallIntegerField()
    living_cost_default = models.PositiveIntegerField()