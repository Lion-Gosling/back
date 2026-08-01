from django.contrib import admin

from benchmarks.models import AgeIncomeBenchmark, RegionPriceStat


@admin.register(RegionPriceStat)
class RegionPriceStatAdmin(admin.ModelAdmin):
    list_display = ('district', 'housing_type', 'eq_rent', 'conversion_rate_annual', 'updated_at')
    list_filter = ('district', 'housing_type')


@admin.register(AgeIncomeBenchmark)
class AgeIncomeBenchmarkAdmin(admin.ModelAdmin):
    list_display = (
        'age_min',
        'age_max',
        'target_asset_default',
        'target_months_default',
        'living_cost_default',
    )