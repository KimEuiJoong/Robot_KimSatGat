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

from django.forms.models import model_to_dict
from django.core import serializers

from .models import User

import random
import requests
#import asyncio
#import aiohttp
import json

# Create your views here.
@api_view(['POST'])
def Login(request):
    req_data = JSONParser().parse(request)
    token = req_data['token']

    url = "https://kapi.kakao.com/v1/user/access_token_info"
    auth = "Bearer " + token
    headers = {"Authorization": auth}
    res = requests.get(url,headers = headers)
    res_json = res.json()
    User(userid=res_json['id'],name=token).save()
    try:
        res.raise_for_status()
        return JsonResponse({"token":token},status = status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"token":"failed"},status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
