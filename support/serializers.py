from rest_framework import serializers

from support.models import SupportProgram


class SupportProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportProgram
        fields = '__all__'