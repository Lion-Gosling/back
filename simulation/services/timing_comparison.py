import copy
import random

from .ai_client import AIServiceError, run_analysis
from .payload_builder import build_analysis_payload


TIMING_VARIANTS = [
    {'label': '지금 독립', 'months': 0},
    {'label': '1년 후 독립', 'months': 12},
    {'label': '2년 후 독립', 'months': 24},
]


def build_timing_comparison(profile, base_scenario) -> dict:
    """base_scenario를 DB에 새로 저장하지 않고 메모리상에서 move_in_after_months만 바꿔
    AI 서버를 시점별로 호출한다. 결과를 하나의 dict로 모아서 반환한다.
    세 변형 모두 같은 seed를 써서, 결과 차이가 조건 차이 때문인지 난수 운 때문인지
    섞이지 않게 한다."""
    shared_seed = random.randint(1, 2_147_483_647)

    results = []
    for variant in TIMING_VARIANTS:
        variant_scenario = copy.copy(base_scenario)
        variant_scenario.move_in_after_months = variant['months']

        payload = build_analysis_payload(
            profile, variant_scenario, profile.target_asset, profile.target_months,
            seed=shared_seed,
        )
        ai_result = run_analysis(payload)  # AIServiceError는 호출부(view)에서 처리

        results.append({
            'label': variant['label'],
            'move_in_after_months': variant['months'],
            'goal_prob': ai_result['goal_probability'],
            'monthly_saving': ai_result['monthly_saving'],
            'trajectory': ai_result['trajectory'],
        })
    return {'variants': results}