from django.urls import path

from . import views

urlpatterns = [
    path('events/analyze/', views.EventAnalyzeView.as_view()),
    path('scenarios/', views.ScenarioCreateView.as_view()),
    path('scenarios/<int:pk>/', views.ScenarioDetailView.as_view()),
    path('diagnoses/', views.DiagnosisCreateView.as_view()),
    path('diagnoses/<int:pk>/', views.DiagnosisDetailView.as_view()),
    path('timing-comparisons/', views.TimingComparisonCreateView.as_view()),
    path('timing-comparisons/<int:pk>/', views.TimingComparisonDetailView.as_view()),
]