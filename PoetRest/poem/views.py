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
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from google.oauth2 import id_token
from google.auth.transport import requests

from .serializers import PoemSerializer,CommentSerializer,LikeSerializer,LikeListSerializer,MyPoemListSerializer,LikeNumSerializer,RecommendListSerializer,AdminPoemSerializer
from django.forms.models import model_to_dict
from django.core import serializers

from django.utils import timezone

from .models import Poem,Comment,Like,Recommendation,Tag,ExPoet,Survey,Feeling,TagScore,PoemTags
from .permissions import IsOwnerOrReadOnly,IsPoemOwnerOrReadOnly
from .recmodel.tagging import tagging

import random
import requests
import json

class AdminPoemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Poem.objects.all()
    serializer_class = AdminPoemSerializer
    expoet = None
    tagTexts = []
    def create(self,request):
        expoetText = request.data['expoet']
        self.tagTexts = request.data['tag']
        self.expoet = ExPoet.objects.get_or_create(name=expoetText)[0]
        return super().create(request)
    def perform_create(self, serializer):
        poem = serializer.save(owner=self.request.user,expoet = self.expoet)
        tags = []
        for tagText in self.tagTexts:
            tags.append(Tag.objects.get(name=tagText))
        for tag in tags:
            pt = PoemTags(poem = poem,tag = tag)
            pt.save()

class PoemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    user_tags = []
    auto_tags = []
    def create(self,request):
        content = request.data['content']
        self.user_tags = request.data['tag']
        if len(self.user_tags) == 0:
            self.auto_tags = tagging(content,"./poem/recmodel/model_v0.4.h5")
        return super().create(request)
    def perform_create(self, serializer):
        poem = serializer.save(owner=self.request.user)
        tags = []
        if len(self.user_tags) == 0:
            for auto_tag in self.auto_tags:
                tags.append(Tag.objects.get(name=auto_tag))
        else:
            for user_tag in self.user_tags:
                tags.append(Tag.objects.get(name=user_tag))
        for tag in tags:
            pt = PoemTags(poem = poem,tag = tag)
            pt.save()

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
        class ConflictButSuccess(APIException):
            status_code = 200
            default_detail = 'Already like this poem'
        try:
            liked_poem = Poem.objects.get(id=self.kwargs['poem_pk'])
            if Like.objects.filter(owner=self.request.user,poem_n=liked_poem).exists():
                return
            else:
                serializer.save(owner=self.request.user,poem_n=liked_poem)
                liked_poem.likenum = F('likenum')+1
                liked_poem.save()
        except IntegrityError as e:
            raise ConflictButSuccess(e)
    def perform_destroy(self, instance):
        liked_poem = instance.poem_n
        if Like.objects.filter(owner=self.request.user,poem_n=liked_poem).exists():
            instance.delete()
            liked_poem.likenum = F('likenum')-1
            liked_poem.save()
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Surveyin(request):
    req_feeling = request.data["feeling"];
    feeling_obj = Feeling.objects.get(name=req_feeling)
    date_now = timezone.localtime(timezone.now()).date()
    if not Survey.objects.filter(owner = request.user,date = date_now).exists():
        Survey.objects.create(owner = request.user,feeling = feeling_obj)
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def LikeFeedback(request):
    FEEDBACK_SCORE = 0.1
    date_now = timezone.localtime(timezone.now()).date()
    survey_feeling = Survey.objects.get(owner = request.user,date = date_now).feeling
    rec_poem = Recommendation.objects.get(owner = request.user,date = date_now).poem_n
    rec_tags = PoemTags.objects.filter(poem=rec_poem).values_list('tag',flat=True)
    #rec_tag = Recommendation.objects.get(owner = request.user,date = date_now).poem_n.tag
    feeling_scores = TagScore.objects.filter(feeling = survey_feeling)
    feedbacks = []
    for rec_tag in rec_tags:
        feedbacks.append(feeling_scores.get(tag=rec_tag))

    if request.method == 'POST':
        feeling_scores.update(score=F('score')-FEEDBACK_SCORE)
        for feedback in feedbacks:
            feedback.score = F('score')+2*FEEDBACK_SCORE
            feedback.save()
    elif request.method == 'DELETE':
        feeling_scores.update(score=F('score')+FEEDBACK_SCORE)
        for feedback in feedbacks:
            feedback.score = F('score')-2*FEEDBACK_SCORE
            feedback.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Recommend(request):

    date_now = timezone.localtime(timezone.now()).date()
    poem_data = None
    if not Recommendation.objects.filter(owner = request.user,date = date_now).exists():
        survey_obj = Survey.objects.get(owner = request.user,date = date_now)
        feeling_obj = survey_obj.feeling
        tagscore = TagScore.objects.filter(feeling = feeling_obj)
        tags = list(tagscore.values_list('tag',flat=True))
        scores = list(tagscore.values_list('score',flat=True))
        randomtag = random.choices(tags,weights=scores)[0]
        rndptags = PoemTags.objects.filter(tag=randomtag)
        rndtagpoemindexes = rndptags.values('poem')
        count = rndtagpoemindexes.aggregate(count=Count('id'))['count']
        rand_i  = random.randrange(0,count)
        randomPoemIndex = rndtagpoemindexes.all()[rand_i]['poem']
        randomPoem = Poem.objects.get(id = randomPoemIndex)
        if not Recommendation.objects.filter(owner = request.user,poem_n = randomPoem).exists():
            newRec = Recommendation(owner = request.user,poem_n = randomPoem)
            newRec.save()
            serializer = PoemSerializer(randomPoem,context={'request':request})
            poem_data = serializer.data
        else:
            pass
    else:
        rec_poem = Recommendation.objects.get(owner=request.user,date=date_now).poem_n
        serializer = PoemSerializer(rec_poem,context={'request':request})
        poem_data = serializer.data
    return JsonResponse(poem_data,safe=False,status = status.HTTP_200_OK)

@api_view(['GET'])
def MyRecommendList(request):
    reclist = Recommendation.objects.filter(owner = request.user).select_related('poem_n')
    serializer = RecommendListSerializer(reclist,context={'request':request},many=True)
    rec_data = serializer.data
    return JsonResponse(rec_data,safe=False,status = status.HTTP_200_OK)

@api_view(['GET'])
def MyLikeList(request):
    likelist = Like.objects.filter(owner = request.user).select_related('poem_n')
    serializer = LikeListSerializer(likelist,context={'request':request},many=True)
    like_data = serializer.data
    return JsonResponse(like_data,safe=False,status = status.HTTP_200_OK)

@api_view(['GET'])
def MyPoemList(request):
    poemlist = Poem.objects.filter(owner = request.user)
    serializer = MyPoemListSerializer(poemlist,context={'request':request},many=True)
    poem_data = serializer.data
    return JsonResponse(poem_data,safe=False,status = status.HTTP_200_OK)

