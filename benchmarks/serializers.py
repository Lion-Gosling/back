from rest_framework import serializers

from benchmarks.models import AgeIncomeBenchmark, RegionPriceStat


class RegionPriceStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionPriceStat
        fields = '__all__'


class AgeIncomeBenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeIncomeBenchmark
        fields = '__all__'