from django.urls import path

from support import views

urlpatterns = [
    path('programs/', views.SupportProgramListView.as_view()),
]