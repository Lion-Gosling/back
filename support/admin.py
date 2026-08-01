from django.contrib import admin

from support.models import SupportProgram


@admin.register(SupportProgram)
class SupportProgramAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'age_min',
		'age_max',
		'income_ratio_min',
		'income_ratio_max',
		'income_max_annual',
		'asset_max',
		'deposit_max',
		'rent_max',
		'is_kb_exclusive',
		'is_kb_available',
	)
	list_filter = ('is_kb_exclusive', 'is_kb_available')
