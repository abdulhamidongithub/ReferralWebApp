from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.conf import settings
from django.core.mail import send_mail
import random

from .models import *

class HomeView(View):
    def get(self, request):
        ref_id = request.GET.get("referrer_id", False)
        referral_link = None
        if request.user.username:
            referral_link = f"{settings.BASE_URL}/?referrer_id={request.user.username}/"
        context = {
            "questions": FAQuestion.objects.all(),
            "referrer_id": ref_id,
            "referral_link": referral_link
        }
        return render(request, 'home.html', context)

    def post(self, request):
        referrer_id = request.POST.get("referrer_id", False)
        referrer = None
        if referrer_id != 'False':
            referrer_id = User.objects.filter(username=referrer_id)
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

class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

class UserDeletion(View):
    def get(self, request):
        return render(request, 'user-deletion.html')

    def post(self, request):
        email = request.POST.get("email")
        waiting_user = WaitingUser.objects.filter(email = email)
        if not waiting_user.exists():
            context = {
                "error": "Email not found in our subscription list"
            }
            return render(request, 'user-deletion.html', context)
        recipient_list = [email]
        code = str(random.randrange(1000000, 9999999))
        waiting_user = waiting_user.first()
        waiting_user.confirmation_code = code
        waiting_user.save()
        email_data = {
            "email_body": "Click to the link below to remove your email: "
                          f"{settings.BASE_URL}/confirm-deletion/{code}/",
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
            "message": "Confirmation link sent to your email"
        }
        return render(request, 'user-deletion.html', context)

class ConfirmDeletion(View):
    def get(self, request, pk):
        waiting_user = WaitingUser.objects.filter(confirmation_code = pk)
        waiting_user.delete()
        context = {
            "message": "Email deleted succesfully"
        }
        return render(request, 'confirmation.html', context)
