from django.shortcuts import render
from django.http import HttpResponse
from .views.CategoryView import CategoryView 
# Create your views here.

def index(request): 
    return HttpResponse("e-Course App")