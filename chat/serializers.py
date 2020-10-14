from rest_framework import serializers

from chat.models import LeadData


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadData
        fields = ('email',)

