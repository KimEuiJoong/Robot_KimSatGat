from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import Poem

#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Poem
#        fields = ('id','email','name')

class PoemSerializer(serializers.ModelSerializer):
    #users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Poem
        fields = ('id','title','writer','content','likenum')
        read_only_fields = ('likenum',)
