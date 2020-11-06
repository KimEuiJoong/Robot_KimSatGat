from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.http.response import JsonResponse
from django.contrib import auth

from django.db.models.aggregates import Count
from django.db.models import F
from django.db.utils import IntegrityError

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from google.oauth2 import id_token
from google.auth.transport import requests

from .serializers import PoemSerializer,CommentSerializer,LikeSerializer,LikeListSerializer,MyPoemListSerializer,LikeNumSerializer
from django.forms.models import model_to_dict
from django.core import serializers

from .models import Poem,Comment,Like
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

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class = LikeSerializer
    def get_queryset(self):
        return Like.objects.filter(poem_n = self.kwargs['poem_pk'])
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset,owner=self.request.user,poem_n=Poem.objects.get(id=self.kwargs['poem_pk']))
        self.check_object_permissions(self.request, obj)
        return obj
    def retrieve(self, retrieve, *args, **kwargs):
        liked_poem = Poem.objects.get(id=self.kwargs['poem_pk'])
        serializer = LikeNumSerializer(liked_poem)
        return Response(serializer.data)

    def perform_create(self, serializer):
        try:
            liked_poem = Poem.objects.get(id=self.kwargs['poem_pk'])
            serializer.save(owner=self.request.user,poem_n=liked_poem)
            liked_poem.likenum = F('likenum')+1
            liked_poem.save()
        except IntegrityError as e:
            class ConflictButSuccess(APIException):
                status_code = 200
                default_detail = 'Already like this poem'
            raise ConflictButSuccess(e)
    def perform_destroy(self, instance):
        liked_poem = instance.poem_n
        instance.delete()
        liked_poem.likenum = F('likenum')-1
        liked_poem.save()


@api_view(['GET'])
def Recommend(request):
    count = Poem.objects.aggregate(count=Count('id'))['count']
    rand_i  = random.randrange(0,count)
    randomPoem = Poem.objects.all()[rand_i]
    poem_data = PoemSerializer(randomPoem).data
    return JsonResponse(poem_data,safe=False,status = status.HTTP_200_OK)

@api_view(['GET'])
def MyLikeList(request):
    likelist = Like.objects.filter(owner = request.user).select_related('poem_n')
    serializer = LikeListSerializer(likelist,many=True)
    like_data = serializer.data
    return JsonResponse(like_data,safe=False,status = status.HTTP_200_OK)

@api_view(['GET'])
def MyPoemList(request):
    poemlist = Poem.objects.filter(owner = request.user)
    serializer = MyPoemListSerializer(poemlist,many=True)
    poem_data = serializer.data
    return JsonResponse(poem_data,safe=False,status = status.HTTP_200_OK)
