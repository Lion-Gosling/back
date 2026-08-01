def slider_to_amounts(eq_rent, rate, slider_pct, min_deposit_floor):
    """슬라이더(0=전세~100=월세) → (보증금, 월세) 환산. 금액 전부 원 단위."""
    deposit_full = eq_rent * 12 / (rate / 100)
    deposit = deposit_full - (deposit_full - min_deposit_floor) * (slider_pct / 100)
    monthly_rent = eq_rent - deposit * (rate / 100) / 12
    return round(deposit), round(monthly_rent)


def calc_dsr_limit(profile, deposit):
    # TODO: 실제 DSR 40% 기준 계산으로 교체 필요. 지금은 임시로 deposit의 60%.
    return round(deposit * 0.6)