from rest_framework import serializers
from .models import PoetTable

class PoetTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoetTable
        fields = ['name','writer','text','cc']
