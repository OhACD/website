from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .tokens import verify_login_token, verify_verification_token
from .services import send_verification_email, send_login_email
from .rate_limit import is_rate_limited

User = get_user_model()

LOGIN_RATE_LIMIT = {"limit": 5, "window": 15 * 60}
REGISTER_RATE_LIMIT = {"limit": 3, "window": 60 * 60}


def _rate_limit_email(request, email, action, limit_config):
    if is_rate_limited(action, email.lower(), limit_config["limit"], limit_config["window"]):
        messages.error(request, "Too many requests. Please try again later.")
        return True
    return False


def register(request):
    if request.method == "GET":
        return render(request, "accounts/register.html")
    # POST
    email = request.POST.get("email")
    name = request.POST.get("name")
    # Gets whether the User want to be part of the mailing list
    mailing_list = bool(request.POST.get("mailing_list"))

    if _rate_limit_email(request, email, "register", REGISTER_RATE_LIMIT):
        return redirect("accounts:register")

    if User.objects.filter(email=email).exists():
        if User.objects.get(email=email).is_verified != True:
            send_verification_email(request, email)
            return HttpResponse("Email already exisits, Check your email to verify")

        messages.error(request, "Email already registered")
        return redirect("accounts:register")

    user = User.objects.create_user(
        email=email,
        name=name,
        mailing_list=mailing_list
        )

    send_verification_email(request, email)
    return HttpResponse("Check your email")

def login_request(request):
    if request.method == "GET":
        return render(request, "accounts/login.html")
    # POST
    email = request.POST.get("email")

    if _rate_limit_email(request, email, "login", LOGIN_RATE_LIMIT):
        return redirect("accounts:login")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "Account Doesn't exist")
        return redirect("accounts:login")

    if not user.is_verified:
        messages.error(request, "Please verify your email address")
        return redirect("accounts:login")
    send_login_email(request, email)
    return HttpResponse("login success, Check your Email")

def verify_email(request):
    token = request.GET.get("token")
    data = verify_verification_token(token)

    if not data:
        return HttpResponse("invalid token")

    user = User.objects.get(email=data.email)
    user.is_verified = True
    user.save()

    return redirect("core:landing")

def login_confirm(request):
    token = request.GET.get("token")
    data = verify_login_token(token)

    if not data:
        return render(request, "accounts/invalid_token.html")
    user = User.objects.get(email=data.email)
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
        return redirect('core:landing')

    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        return redirect('core:landing')

    return redirect('core:landing')
