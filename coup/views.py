import os

from django.shortcuts import render
from coup.settings import BASE_DIR

def index(request):
    return render(request, 'index.html')