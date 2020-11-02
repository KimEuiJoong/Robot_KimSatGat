from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http.response import JsonResponse
from django.contrib import auth

from django.db.models.aggregates import Count

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from google.oauth2 import id_token
from google.auth.transport import requests

from .serializers import PoemSerializer,CommentSerializer
from django.forms.models import model_to_dict
from django.core import serializers

from .models import Poem,Comment
from .permissions import IsOwnerOrReadOnly,IsPoemOwnerOrReadOnly

import random
import requests
import json


class PoemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsPoemOwnerOrReadOnly)
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.filter(poem_n = self.kwargs['poem_pk']).select_related('owner')
        #return Comment.objects.filter(poem_n = self.kwargs['poem_pk']).select_related('owner')
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,id=self.kwargs['comment_pk'])
        self.check_object_permissions(self.request, obj)
        return obj
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,poem_n=Poem.objects.get(id=self.kwargs['poem_pk']))

@api_view(['GET'])
def Recommend(request):
    count = Poem.objects.aggregate(count=Count('id'))['count']
    rand_i  = random.randrange(0,count)
    randomPoem = Poem.objects.all()[rand_i]
    poem_data = PoemSerializer(randomPoem).data
    return JsonResponse(poem_data,safe=False,status = status.HTTP_201_CREATED)
