from django.shortcuts import render

from django.http.response import JsonResponse
from django.contrib import auth

from django.db.models.aggregates import Count

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

from django.forms.models import model_to_dict
from django.core import serializers

from .models import User

import random
import requests
#import asyncio
#import aiohttp
import json

@api_view(['POST'])
def Login(request):
    req_data = JSONParser().parse(request)
    token = req_data['token']
    name = req_data['name']
    url = "https://kapi.kakao.com/v1/user/access_token_info"
    auth = "Bearer " + token
    headers = {"Authorization": auth}
    res = requests.get(url,headers = headers)
    res_json = res.json()
    userid = res_json['id']

    try:
        user = User.objects.get(userid=userid)
    except:
        User(userid=userid,name=name).save()
        user = User.objects.get(userid=userid)
    satgatToken = Token.objects.get_or_create(user=user)
    try:
        res.raise_for_status()
        return JsonResponse({"token":satgatToken[0].key},status = status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"token":"failed"},status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
