from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import Profile
from simulation.models import Scenario

from support.serializers import SupportProgramSerializer
from support.utils import match_programs


class SupportProgramListView(APIView):
	def get(self, request):
		profile_id = request.query_params.get('profile_id')
		scenario_id = request.query_params.get('scenario_id')

		profile = get_object_or_404(Profile, pk=profile_id)
		scenario = Scenario.objects.filter(pk=scenario_id).first() if scenario_id else None

		matched = match_programs(profile, scenario)
		return Response(SupportProgramSerializer(matched, many=True).data)
