from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.conf import settings
from django.core.mail import send_mail

from .models import *

class HomeView(View):
    def get(self, request):
        ref_id = request.GET.get("referrer_id", False)
        context = {
            "questions": FAQuestion.objects.all(),
            "referrer_id": ref_id
        }
        return render(request, 'home.html', context)

    def post(self, request):
        referrer_id = request.POST.get("referrer_id", False)
        referrer = None
        if referrer_id != 'False':
            referrer_id = User.objects.filter(id=referrer_id)
            if referrer_id.exists():
                referrer = referrer_id.first()
        waiting_user = WaitingUser.objects.filter(
            email = request.POST.get("email")
        )
        if waiting_user.exists():
            context = {
                "questions": FAQuestion.objects.all(),
                "error": "This email owner has already subscribed!"
            }
            return render(request, 'home.html', context)
        waiting_user = WaitingUser.objects.create(
            email = request.POST.get("email"),
            referrer = referrer
        )
        recipient_list = [waiting_user.email]
        email_data = {
            "email_body": "You have successfully subscribed "
                          "to our referral app!",
            "to_email": recipient_list,
            "email_subject": "Subscription to the referral app",
        }
        send_mail(
            email_data["email_subject"],
            message=email_data["email_body"],
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=email_data["to_email"],
        )
        context = {
            "questions": FAQuestion.objects.all(),
            "success_message": "Email successfully added!"
        }
        return render(request, 'home.html', context)

class SubPageView(View):
    def get(self, request):
        return render(request, 'sub-page.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user = User.objects.filter(username = request.POST.get("username"))
        if user.exists():
            return render(
                request,
                "register.html",
                {"error": "This username is not available"}
            )
        user = User.objects.create(
            username = request.POST.get("username"),
            email = request.POST.get("email"),
            password = request.POST.get("password"),
            is_superuser = False,
            is_staff = False
        )
        user.referral_link = settings.BASE_URL + f'/?referrer_id={user.id}'
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