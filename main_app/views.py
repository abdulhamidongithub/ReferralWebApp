from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.conf import settings

from .models import *

class HomeView(View):
    def get(self, request):
        context = {
            "questions": FAQuestion.objects.all()
        }
        return render(request, 'home.html', context)

class SubPageView(View):
    def get(self, request):
        return render(request, 'sub-page.html')

class RegisterView(View):
    def get(self, request):
        ref_id = request.GET.get("referrer_id", "none")
        context = {
            "referrer_id": ref_id
        }
        return render(request, 'register.html', context)

    def post(self, request):
        referrer_id = request.POST.get("referrer_id")
        user = User.objects.filter(username = request.POST.get("username"))
        if user.exists():
            return render(
                request,
                "register.html",
                {"error": "This username is not available", "referrer_id": referrer_id}
            )
        referrer = None
        if referrer_id != "none":
            referrer_id = User.objects.filter(id = referrer_id)
            if referrer_id.exists():
                referrer = referrer_id.first()
        user = User.objects.create(
            username = request.POST.get("username"),
            email = request.POST.get("email"),
            password = request.POST.get("password"),
            is_superuser = False,
            is_staff = False,
            referrer = referrer
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