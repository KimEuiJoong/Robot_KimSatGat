from django.shortcuts import render

from django.http.response import JsonResponse
from django.contrib import auth

from django.db.models.aggregates import Count

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import permissions

from google.oauth2 import id_token
from google.auth.transport import requests

from .serializers import UserSerializer,PoemSerializer
from django.forms.models import model_to_dict
from django.core import serializers

from .models import Poem
from .models import User

import random

class PoemViewSet(viewsets.ModelViewSet):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    #permission_classes = [permissions.IsAuthenticated]

@api_view(['GET'])
def Recommend(request):
    count = Poem.objects.aggregate(count=Count('id'))['count']
    rand_i  = random.randrange(0,count)
    randomPoem = Poem.objects.all()[rand_i]
    data = serializers.serialize("json",[randomPoem],ensure_ascii=False)
    return JsonResponse(data,safe=False,status = status.HTTP_201_CREATED)
    
@api_view(['POST'])
def ManualSignUp(request):
    req_data = JSONParser().parse(request)
    email = req_data['email']
    name = req_data['name']
    User.objects.create_user(email = email,name=name)
    auth.login(request,user)

    

