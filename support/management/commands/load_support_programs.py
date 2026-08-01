from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from support.models import SupportProgram


class Command(BaseCommand):
    help = 'Load support programs from data/support_programs.csv'

    def handle(self, *args, **options):
        csv_path = Path(settings.BASE_DIR) / 'data' / 'support_programs.csv'
        rows = self._read_csv(csv_path)
        programs = [self._build_program(row) for row in rows]

        with transaction.atomic():
            SupportProgram.objects.all().delete()
            SupportProgram.objects.bulk_create(programs)

        self.stdout.write(self.style.SUCCESS('Support programs loaded successfully.'))

    def _read_csv(self, csv_path: Path):
        if not csv_path.exists():
            raise CommandError(f'CSV file not found: {csv_path}')

        with csv_path.open(newline='', encoding='utf-8-sig') as csv_file:
            return list(DictReader(csv_file))

    def _build_program(self, row):
        return SupportProgram(
            name=row['name'],
            age_min=int(row['age_min']),
            age_max=int(row['age_max']),
            income_ratio_min=self._to_float(row.get('income_ratio_min')),
            income_ratio_max=self._to_float(row.get('income_ratio_max')),
            income_max_annual=self._to_int(row.get('income_max_annual')),
            asset_max=self._to_int(row.get('asset_max')),
            deposit_max=self._to_int(row.get('deposit_max')),
            rent_max=self._to_int(row.get('rent_max')),
            benefit_desc=row['benefit_desc'],
            source_url=row['source_url'],
            is_kb_exclusive=self._to_bool(row.get('is_kb_exclusive')),
            is_kb_available=self._to_bool(row.get('is_kb_available')),
        )

    def _to_int(self, value):
        if value in (None, ''):
            return None
        return int(value)

    def _to_float(self, value):
        if value in (None, ''):
            return None
        return float(value)

    def _to_bool(self, value):
        return str(value).strip().lower() in {'1', 'true', 'yes', 'y'}