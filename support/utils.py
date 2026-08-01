from support.models import SupportProgram


MEDIAN_INCOME_1PERSON_MONTHLY = 2564238  # 2026년 1인가구 기준중위소득(원/월)


def match_programs(profile, scenario=None):
    annual_income = profile.monthly_income * 12
    matched = []

    for program in SupportProgram.objects.all():
        if not (program.age_min <= profile.age <= program.age_max):
            continue

        if program.income_ratio_max is not None:
            ratio = (annual_income / (MEDIAN_INCOME_1PERSON_MONTHLY * 12)) * 100
            if program.income_ratio_min is not None and ratio < program.income_ratio_min:
                continue
            if ratio > program.income_ratio_max:
                continue
        elif program.income_max_annual is not None:
            if annual_income > program.income_max_annual:
                continue

        if program.asset_max is not None and profile.current_cash > program.asset_max:
            continue

        if scenario is not None:
            if program.deposit_max is not None and scenario.deposit > program.deposit_max:
                continue
            if program.rent_max is not None and scenario.monthly_rent > program.rent_max:
                continue

        matched.append(program)

    return matched