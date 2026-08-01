from django.urls import path

from profiles.views import ProfileCreateView, ProfileDetailView, ProfileEventAnswersView

urlpatterns = [
    path('financial-profiles/', ProfileCreateView.as_view(), name='profile-create'),
    path('financial-profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('<int:pk>/events/', ProfileEventAnswersView.as_view(), name='profile-event-answers'),
]