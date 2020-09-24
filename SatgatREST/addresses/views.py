from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Create your views here.

@csrf_exempt
def poet(request):
    return HttpResponse('Hello world')