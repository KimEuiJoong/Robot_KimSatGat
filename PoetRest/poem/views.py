from django.shortcuts import render

from django.http.response import JsonResponse

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import permissions

from google.oauth2 import id_token
from google.auth.transport import requests

from .serializers import UserSerializer,PoemSerializer

from .models import Poem

class PoemViewSet(viewsets.ModelViewSet):
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    #permission_classes = [permissions.IsAuthenticated]
