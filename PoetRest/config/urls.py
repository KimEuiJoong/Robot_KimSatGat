"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
import sociallogin.views as sviews
from poem.views import PoemViewSet

poem_list =  PoemViewSet.as_view({
    'post':'create'
})
poem = PoemViewSet.as_view({
    'post':'create',
    'get':'retrieve',
    'put':'update',
    'delete':'destroy'
})

urlpatterns = format_suffix_patterns([
    path('admin/', admin.site.urls),
    path('sociallogin/glogintoken', sviews.GLoginTokenAuth),
    path('poems',poem_list, name='poem_list'),
    path('poems/<int:pk>',poem,name='poem'),
])
