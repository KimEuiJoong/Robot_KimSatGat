import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from poem.views import PoemViewSet,CommentViewSet,LikeViewSet,Recommend,MyLikeList,MyPoemList,MyRecommendList,AdminPoemViewSet
from account.views import Login

poem_list =  PoemViewSet.as_view({
    'post':'create'
})
poem = PoemViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy'
})
comment_list =  CommentViewSet.as_view({
    'post':'create',
    'get':'list'
})
comment = CommentViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'delete':'destroy'
})
like =  LikeViewSet.as_view({
    'post':'create',
    'get':'retrieve',
    'delete':'destroy'
})
adminpoem = AdminPoemViewSet.as_view({
    'post':'create'
})

urlpatterns = format_suffix_patterns([
    path('admin/', admin.site.urls),
    path('logintoken',Login),
    path('poems',poem_list, name='poem_list'),
    path('poems/<int:pk>',poem,name='poem'),
    path('poems/<int:poem_pk>/comments',comment_list, name='comment_list'),
    path('poems/<int:poem_pk>/comments/<int:comment_pk>',comment, name='comment'),
    path('poems/<int:poem_pk>/like',like, name='like'),
    path('poems/recommended', Recommend),
    path('poems/mylikelist', MyLikeList),
    path('poems/mypoemlist', MyPoemList),
    path('poems/myrecommendlist', MyRecommendList),
    path('poems/admin', adminpoem,name = 'adminpoem'),
])
