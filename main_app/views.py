from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.conf import settings

from .models import *

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class SubPageView(View):
    def get(self, request):
        return render(request, 'sub-page.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user = User.objects.filter(username = request.POST.get("username"))
        if user.exists():
            return render(request, "register.html", {"error": "This username is not available"})
        user = User.objects.create(
            username = request.POST.get("username"),
            email = request.POST.get("email"),
            password = request.POST.get("password"),
            is_superuser = False,
            is_staff = False
        )
        user.referral_link = settings.BASE_URL + f'/register/?referrer_id={user.id}'
        user.save()
        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = User.objects.filter(
            username = request.POST.get("username"),
            password = request.POST.get("password")
        )
        if user.exists():
            user = user.first()
            login(request, user)
            return redirect("home")
        return render(request, 'login.html', {"error": "Username or password is incorrect"})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")