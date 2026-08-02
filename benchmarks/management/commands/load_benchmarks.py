from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from benchmarks.models import AgeIncomeBenchmark, RegionPriceStat


class Command(BaseCommand):
    help = 'Load benchmark data from data/region_price_stat.csv and data/age_income_benchmark.csv'

    def handle(self, *args, **options):
        data_dir = Path(settings.BASE_DIR) / 'data'
        region_path = data_dir / 'region_price_stat.csv'
        age_path = data_dir / 'age_income_benchmark.csv'

        self._load_region_price_stat(region_path)
        self._load_age_income_benchmark(age_path)

        self.stdout.write(self.style.SUCCESS('Benchmarks loaded successfully.'))

    def _load_region_price_stat(self, csv_path: Path):
        rows = self._read_csv(csv_path)
        objects = [
            RegionPriceStat(
                district=row['district'],
                housing_type=row['housing_type'],
                eq_rent=int(row['eq_rent']),
                conversion_rate_annual=float(row['conversion_rate_annual']),
                min_deposit_floor=int(row['min_deposit_floor']),
                default_slider_pct=int(row['default_slider_pct']),
                moving_cost_avg=int(row['moving_cost_avg']),
                brokerage_fee_avg=int(row['brokerage_fee_avg']),
            )
            for row in rows
        ]

        with transaction.atomic():
            RegionPriceStat.objects.all().delete()
            RegionPriceStat.objects.bulk_create(objects)

    def _load_age_income_benchmark(self, csv_path: Path):
        rows = self._read_csv(csv_path)
        objects = [
            AgeIncomeBenchmark(
                age_min=int(row['age_min']),
                age_max=int(row['age_max']),
                target_asset_default=int(row['target_asset_default']),
                target_months_default=int(row['target_months_default']),
                living_cost_default=int(row['living_cost_default']),
                monthly_income_default=int(row['monthly_income_default'])
            )
            for row in rows
        ]

        with transaction.atomic():
            AgeIncomeBenchmark.objects.all().delete()
            AgeIncomeBenchmark.objects.bulk_create(objects)

    def _read_csv(self, csv_path: Path):
        if not csv_path.exists():
            raise CommandError(f'CSV file not found: {csv_path}')

        with csv_path.open(newline='', encoding='utf-8-sig') as csv_file:
            return list(DictReader(csv_file))