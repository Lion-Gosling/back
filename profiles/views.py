from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileCreateView(generics.CreateAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveAPIView):
	queryset = Profile.objects.all()
	serializer_class = ProfileSerializer


class ProfileEventAnswersView(APIView):
	def patch(self, request, pk):
		profile = get_object_or_404(Profile, pk=pk)
		answers = request.data.get('event_answers', [])
		profile.event_answers = answers
		profile.save(update_fields=['event_answers'])
		return Response({'id': profile.id, 'event_answers': profile.event_answers})
