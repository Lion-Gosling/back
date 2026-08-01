from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from benchmarks.models import RegionPriceStat
from profiles.models import Profile

from .models import Diagnosis, Scenario, TimingComparison
from .serializers import (
    DiagnosisSerializer,
    ScenarioCreateSerializer,
    ScenarioSerializer,
    TimingComparisonSerializer,
)
from .services.ai_client import AIServiceError, analyze_events, run_analysis
from .services.payload_builder import build_analysis_payload
from .services.timing_comparison import build_timing_comparison
from .utils import calc_dsr_limit, slider_to_amounts


class ScenarioCreateView(APIView):
    def post(self, request):
        input_serializer = ScenarioCreateSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        profile = get_object_or_404(Profile, pk=data['profile_id'])
        stat = get_object_or_404(
            RegionPriceStat,
            district=data['district'],
            housing_type=data['housing_type'],
        )

        deposit, monthly_rent = slider_to_amounts(
            stat.eq_rent,
            stat.conversion_rate_annual,
            data['contract_slider_pct'],
            stat.min_deposit_floor,
        )

        loan_amount = calc_dsr_limit(profile, deposit) if data['wants_loan'] else 0

        scenario = Scenario.objects.create(
            profile=profile,
            district=data['district'],
            housing_type=data['housing_type'],
            contract_slider_pct=data['contract_slider_pct'],
            deposit=deposit,
            monthly_rent=monthly_rent,
            moving_cost=stat.moving_cost_avg,
            brokerage_fee=stat.brokerage_fee_avg,
            conversion_rate_annual=stat.conversion_rate_annual,
            deposit_loan_amount=loan_amount,
            loan_interest_rate=0.045 if loan_amount > 0 else 0.0,
            loan_repayment_type='interest_only' if loan_amount > 0 else 'none',
            scenario_type='move_now',
            move_in_after_months=0,
        )
        return Response(ScenarioSerializer(scenario).data, status=201)


class ScenarioDetailView(generics.RetrieveAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer


class DiagnosisCreateView(APIView):
    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        if not scenario_id:
            return Response({'detail': 'scenario_id는 필수입니다.'}, status=400)

        scenario = get_object_or_404(Scenario, pk=scenario_id)
        profile = scenario.profile

        payload = build_analysis_payload(
            profile, scenario, profile.target_asset, profile.target_months
        )
        try:
            ai_result = run_analysis(payload)
        except AIServiceError as exc:
            return Response({'message': str(exc), 'detail': exc.detail}, status=exc.status_code)

        diagnosis = Diagnosis.objects.create(
            profile=profile,
            scenario=scenario,
            scenario_id_ai=ai_result.get('scenario_id', ''),
            achievement_score=ai_result.get('achievement_score'),
            suitability=ai_result.get('suitability', ''),
            goal_probability=ai_result.get('goal_probability'),
            district=scenario.district,
            housing_type=scenario.housing_type,
            raw_payload=ai_result,
        )
        return Response({'id': diagnosis.id, **ai_result}, status=201)


class DiagnosisDetailView(generics.RetrieveAPIView):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer


class TimingComparisonCreateView(APIView):
    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        if not scenario_id:
            return Response({'detail': 'scenario_id는 필수입니다.'}, status=400)

        scenario = get_object_or_404(Scenario, pk=scenario_id)
        profile = scenario.profile

        try:
            result = build_timing_comparison(profile, scenario)
        except AIServiceError as exc:
            return Response({'message': str(exc), 'detail': exc.detail}, status=exc.status_code)

        comparison = TimingComparison.objects.create(
            profile=profile,
            base_scenario=scenario,
            raw_payload=result,
        )
        return Response({'id': comparison.id, **result}, status=201)


class TimingComparisonDetailView(generics.RetrieveAPIView):
    queryset = TimingComparison.objects.all()
    serializer_class = TimingComparisonSerializer


class EventAnalyzeView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        if not (1 <= len(text) <= 500):
            return Response({'detail': 'text는 1~500자여야 합니다.'}, status=400)
        try:
            result = analyze_events(text)
        except AIServiceError as exc:
            return Response({'message': str(exc), 'detail': exc.detail}, status=exc.status_code)
        return Response(result)