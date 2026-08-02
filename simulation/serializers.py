from rest_framework import serializers

from .models import Diagnosis, Scenario, TimingComparison

PYEONG_TO_M2 = 3.3058

class ScenarioCreateSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()
    district = serializers.ChoiceField(choices=Scenario._meta.get_field('district').choices)
    housing_type = serializers.ChoiceField(choices=[('아파트', '아파트'), ('오피스텔', '오피스텔'), ('연립·다세대', '연립·다세대')])
    contract_slider_pct = serializers.IntegerField(min_value=0, max_value=100)
    wants_loan = serializers.BooleanField(default=False)
    desired_area_pyeong = serializers.FloatField(min_value=3, max_value=18.1) 

class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['desired_area_pyeong'] = round(instance.desired_area_m2 / PYEONG_TO_M2, 1)
        return data

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class TimingComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimingComparison
        fields = '__all__'