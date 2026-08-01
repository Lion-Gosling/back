from rest_framework import serializers

from .models import Diagnosis, Scenario, TimingComparison


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'


class ScenarioCreateSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    district = serializers.ChoiceField(choices=Scenario._meta.get_field('district').choices)
    housing_type = serializers.ChoiceField(choices=[('아파트', '아파트'), ('오피스텔', '오피스텔'), ('연립·다세대', '연립·다세대')])
    contract_slider_pct = serializers.IntegerField(min_value=0, max_value=100)
    wants_loan = serializers.BooleanField(default=False)


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class TimingComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingComparison
        fields = '__all__'