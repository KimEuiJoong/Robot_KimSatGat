from django.shortcuts import render

from django.http.response import JsonResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from google.oauth2 import id_token
from google.auth.transport import requests


from .serializers import GLoginTokenSerializer
from .models import GLoginToken

@api_view(['POST'])
def GLoginTokenAuth(request):
    req_data = JSONParser().parse(request)
    token = req_data['idToken']
    print(req_data)
    queryset = GLoginToken.objects.all()
    serializer = GLoginTokenSerializer(data = req_data)
    if serializer.is_valid():
        #serializer.save()
        try:
            print(token)
            idinfo = id_token.verify_oauth2_token(token, requests.Request(),"607479431956-e9r2gdgjqfd8bhnfn3e5o9o6ohsia5qq.apps.googleusercontent.com")
            print(idinfo['sub'])
        except ValueError:
            print("valueError")
            pass
        return JsonResponse(serializer.data,status = status.HTTP_201_CREATED)    
    return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
