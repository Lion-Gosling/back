from django.db import models


class SupportProgram(models.Model):
	name = models.CharField(max_length=100)
	age_min = models.PositiveSmallIntegerField()
	age_max = models.PositiveSmallIntegerField()
	income_ratio_min = models.FloatField(null=True, blank=True)
	income_ratio_max = models.FloatField(null=True, blank=True)
	income_max_annual = models.PositiveIntegerField(null=True, blank=True)
	asset_max = models.PositiveIntegerField(null=True, blank=True)
	deposit_max = models.PositiveIntegerField(null=True, blank=True)
	rent_max = models.PositiveIntegerField(null=True, blank=True)
	benefit_desc = models.CharField(max_length=200)
	source_url = models.URLField()
	is_kb_exclusive = models.BooleanField(default=False)
	is_kb_available = models.BooleanField(default=False)

	class Meta:
		ordering = ['-is_kb_exclusive', 'name']
