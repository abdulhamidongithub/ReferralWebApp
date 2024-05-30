from django.shortcuts import render
from django.views import View

from .models import *

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class SubPageView(View):
    def get(self, request):
        return render(request, 'sub-page.html')
