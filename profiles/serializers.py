from rest_framework import serializers

from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def validate_age(self, value):
        if not 19 <= value <= 100:
            raise serializers.ValidationError('나이는 19~100 사이여야 합니다.')
        return value

    def validate_monthly_income(self, value):
        if value <= 0:
            raise serializers.ValidationError('월소득은 0보다 커야 합니다.')
        return value

    def validate_current_cash(self, value):
        if value <= 0:
            raise serializers.ValidationError('보유 자산은 0보다 커야 합니다.')
        return value

    def validate_target_asset(self, value):
        if value <= 0:
            raise serializers.ValidationError('목표자산은 0보다 커야 합니다.')
        return value