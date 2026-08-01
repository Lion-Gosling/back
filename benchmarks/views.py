from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from benchmarks.models import AgeIncomeBenchmark, RegionPriceStat
from benchmarks.serializers import (
    AgeIncomeBenchmarkSerializer,
    RegionPriceStatSerializer,
)


class RegionPriceStatView(APIView):
    def get(self, request):
        district = request.query_params.get('district')
        housing_type = request.query_params.get('housing_type')

        if not district or not housing_type:
            return Response({'detail': 'district와 housing_type이 필요합니다.'}, status=400)

        obj = get_object_or_404(RegionPriceStat, district=district, housing_type=housing_type)
        return Response(RegionPriceStatSerializer(obj).data)


class AgeIncomeBenchmarkView(APIView):
    def get(self, request):
        age = request.query_params.get('age')

        if age is None:
            return Response({'detail': 'age가 필요합니다.'}, status=400)

        try:
            age = int(age)
        except ValueError:
            return Response({'detail': 'age는 정수여야 합니다.'}, status=400)

        obj = AgeIncomeBenchmark.objects.filter(
            age_min__lte=age,
            age_max__gte=age,
        ).first()

        if not obj:
            return Response({'detail': '해당 구간의 벤치마크가 없습니다.'}, status=404)

        return Response(AgeIncomeBenchmarkSerializer(obj).data)