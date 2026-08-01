from django.urls import path

from benchmarks.views import AgeIncomeBenchmarkView, RegionPriceStatView

urlpatterns = [
    path('housing/', RegionPriceStatView.as_view()),
    path('targets/', AgeIncomeBenchmarkView.as_view()),
]