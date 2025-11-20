from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from .tokens import generate_login_token, generate_verification_token, verify_login_token, verify_verification_token
from django.contrib.admin.views.decorators import staff_member_required
from dotenv import load_dotenv
import os

load_dotenv()

# Host Email
sender = os.getenv("EMAIL_HOST_USER")

User = get_user_model()

# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")
    # POST
    email = request.POST.get("email")
    name = request.POST.get("name")
    # Gets whether the User want to be part of the mailing list
    mailing_list = request.POST.get("mailing_list")
    if mailing_list == None:
        mailing_list = False

    if User.objects.filter(email=email).exists():
        if User.objects.get(email=email).is_verified != True:
            token = generate_verification_token({"email": email})
            url = request.build_absolute_uri(reverse("accounts:verify") + f"?token={token}")
            send_mail(
                "Verify your account",
                f"Click to verify your email:\n\n{url}",
                sender,
                [email],
                )
            return HttpResponse("Email already exisits, Check your email to verify")

        messages.error(request, "Email already registered")
        return redirect("accounts:register")

    user = User.objects.create_user(
        email=email,
        name=name,
        mailing_list=mailing_list
        )

    # Send the Verification Email Might extract into a seperate Helper method
    token = generate_verification_token({"email": email})
    url = request.build_absolute_uri(reverse("accounts:verify") + f"?token={token}")
    send_mail(
        "Verify your account",
        f"Click to verify your email:\n\n{url}",
        sender,
        [email],
        fail_silently=False
    )
    return HttpResponse("Check your email")

def login_request(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")
    # POST
    email = request.POST.get("email")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "Account Doesn't exist")
        return redirect("accounts:login")

    if not user.is_verified:
        messages.error("Please verify your email address")
        return redirect("accounts:login")
    token = generate_login_token({"email": email})
    url = request.build_absolute_uri(reverse("accounts:login_confirm") + f"?token={token}")
    send_mail(
        "Your login link",
        f"Click here to log in:\n\n{url}",
        sender,
        [email],
        fail_silently=False
    )
    return HttpResponse("login success, Check your Email")

def verify_email(request):
    token = request.GET.get("token")
    data = verify_verification_token(token)

    if not data:
        return HttpResponse("invalid token")

    user = User.objects.get(email=data["email"])
    user.is_verified = True
    user.save()

    return redirect("core:landing")

def login_confirm(request):
    token = request.GET.get("token")
    data = verify_login_token(token)

    if not data:
        return render(request, "accounts/invalid_token.html")
    user = User.objects.get(email=data["email"])
    login(request, user)
    return redirect("core:landing")

def logout_view(request):
    logout(request)
    return redirect("core:landing")

# Endpoint to delete users
@staff_member_required
def delete_user(request, email):
    try:
        user = User.objects.get(email=email)
        user.delete()
        messages.success(request, "User deleted")

    except User.DoesNotExist:
        messages.error(request, "User dosn't exist")
        return render(request, 'core:landing')

    except Exception as e:
        return render(request, 'core:landing',{'error':e.message})

    return render(request, 'core:landing')
