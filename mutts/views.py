from django.http import HttpResponse
from django.shortcuts import render


def about(request):
   return HttpResponse('about.html')

def home(request):
   return HttpResponse('homepage.html')