from django.conf import settings
import random

def build_analysis_payload(profile, scenario, target_asset, target_months, n_sims=5000, seed=None):
    if seed is None:
        seed = random.randint(1, 2_147_483_647)
    return {
        'basic_info': {
            'age': profile.age,
            'monthly_income': profile.monthly_income,
            'current_assets': profile.current_cash,
            'monthly_living_expense': profile.monthly_living_cost,
            'current_monthly_housing_cost': profile.current_monthly_housing_cost,
            'savings_interest_rate_annual': settings.SAVINGS_INTEREST_RATE_ANNUAL,
            'existing_loan': {
                'balance': profile.debt_balance,
                'monthly_payment': profile.debt_monthly_payment,
                'annual_interest_rate': getattr(profile, 'existing_loan_interest_rate', 0.0),
                'remaining_months': getattr(profile, 'existing_loan_remaining_months', 0),
                'repayment_type': getattr(profile, 'existing_loan_repayment_type', 'none'),
            },
        },
        'desired_housing': {
            'housing_type': scenario.housing_type,
            'tenure_type': scenario.contract_type,
            'district': scenario.district,
            'desired_area_m2': getattr(scenario, 'desired_area_m2', 35.0),
            'desired_deposit': scenario.deposit,
            'desired_monthly_rent': 0 if scenario.contract_type == 'jeonse' else scenario.monthly_rent,
            'move_in_after_months': scenario.move_in_after_months,
            'deposit_loan_amount': scenario.deposit_loan_amount,
            'loan_interest_rate': scenario.loan_interest_rate,
            'loan_repayment_type': scenario.loan_repayment_type,
            'moving_cost': scenario.moving_cost,
            'brokerage_fee': scenario.brokerage_fee,
            'monthly_support': scenario.monthly_support,
            'support_months': scenario.support_months,
            'deposit_return_rate': scenario.deposit_return_rate,
            'conversion_rate_annual': scenario.conversion_rate_annual / 100,
            'contract_months': scenario.contract_months,
        },
        'goal': {'target_asset': target_asset, 'target_months': target_months},
        'event_answers': profile.event_answers,
        'n_sims': n_sims,
        'seed': seed,
    }