from rest_framework import serializers
from .models import GLoginToken

class GLoginTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLoginToken
        fields = ['idToken']