"""
Views for the accounts app.

This module handles user registration, login, email verification, and logout
functionality using passwordless (magic link) authentication.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
import logging

from .tokens import verify_login_token, verify_verification_token
from .services import send_verification_email, send_login_email
from .rate_limit import is_rate_limited

User = get_user_model()
logger = logging.getLogger(__name__)

# Rate limiting configuration
LOGIN_RATE_LIMIT = {"limit": 5, "window": 15 * 60}  # 5 requests per 15 minutes
REGISTER_RATE_LIMIT = {"limit": 3, "window": 60 * 60}  # 3 requests per hour


def _rate_limit_email(request, email, action, limit_config):
    """
    Check and enforce rate limiting for email-based actions.

    Args:
        request: Django request object
        email: Email address to check
        action: Action identifier (e.g., "login", "register")
        limit_config: Dictionary with "limit" and "window" keys

    Returns:
        True if rate limited, False otherwise
    """
    if is_rate_limited(action, email.lower(), limit_config["limit"], limit_config["window"]):
        messages.error(request, "Too many requests. Please try again later.")
        return True
    return False


def _validate_email(email):
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str | None)
    """
    if not email:
        return False, "Email is required."
    try:
        validate_email(email)
        return True, None
    except ValidationError:
        return False, "Please enter a valid email address."


def _validate_name(name):
    """
    Validate name field.

    Args:
        name: Name string to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str | None)
    """
    if not name:
        return False, "Name is required."
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long."
    if len(name.strip()) > 255:
        return False, "Name must be less than 255 characters."
    return True, None


def register(request):
    """
    Handle user registration.

    GET: Display registration form
    POST: Process registration, create user, and send verification email

    Returns:
        Rendered template (GET) or redirect (POST)
    """
    if request.method == "GET":
        return render(request, "accounts/register.html")

    # POST
    email = request.POST.get("email", "").strip()
    name = request.POST.get("name", "").strip()
    # Gets whether the User want to be part of the mailing list
    mailing_list = bool(request.POST.get("mailing_list"))

    # Validate email format
    is_valid, error_msg = _validate_email(email)
    if not is_valid:
        messages.error(request, error_msg)
        return redirect("accounts:register")

    # Validate name
    is_valid, error_msg = _validate_name(name)
    if not is_valid:
        messages.error(request, error_msg)
        return redirect("accounts:register")

    # Rate limiting
    if _rate_limit_email(request, email, "register", REGISTER_RATE_LIMIT):
        return redirect("accounts:register")

    # Check if user already exists
    try:
        existing_user = User.objects.get(email=email)
        if not existing_user.is_verified:
            # User exists but not verified - resend verification email
            try:
                send_verification_email(request, email)
                messages.info(request, "This email is already registered but not verified. We've sent a new verification email. Please check your inbox.")
            except Exception as e:
                logger.error(f"Failed to send verification email: {e}")
                messages.error(request, "This email is already registered but not verified. We couldn't send a verification email. Please try again later.")
            return redirect("accounts:register")
        else:
            # User exists and is verified
            messages.error(request, "This email is already registered. Please log in instead.")
            return redirect("accounts:register")
    except User.DoesNotExist:
        # User doesn't exist - create new user
        pass

    # Create new user
    try:
        user = User.objects.create_user(
            email=email,
            name=name,
            mailing_list=mailing_list
        )

        # Send verification email
        try:
            send_verification_email(request, email)
            messages.success(request, "Registration successful! Please check your email to verify your account.")
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            messages.warning(request, "Account created, but we couldn't send the verification email. Please contact support.")
    except IntegrityError as e:
        logger.error(f"Integrity error creating user: {e}")
        messages.error(request, "An error occurred during registration. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        messages.error(request, "An unexpected error occurred. Please try again later.")

    return redirect("accounts:register")

def login_request(request):
    """
    Handle login requests via magic link.

    GET: Display login form
    POST: Send magic link email to user

    Returns:
        Rendered template (GET) or redirect (POST)
    """
    if request.method == "GET":
        return render(request, "accounts/login.html")

    # POST
    email = request.POST.get("email", "").strip()

    # Check if user is already logged in
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("core:landing")

    # Validate email format
    is_valid, error_msg = _validate_email(email)
    if not is_valid:
        messages.error(request, error_msg)
        return redirect("accounts:login")

    # Rate limiting
    if _rate_limit_email(request, email, "login", LOGIN_RATE_LIMIT):
        return redirect("accounts:login")

    # Check if user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "No account found with this email address. Please register first.")
        return redirect("accounts:login")

    # Check if user is verified
    if not user.is_verified:
        messages.warning(request, "Please verify your email address before logging in. Check your inbox for the verification link.")
        return redirect("accounts:login")

    # Send login email
    try:
        send_login_email(request, email)
        messages.success(request, "Login link sent! Please check your email.")
    except Exception as e:
        logger.error(f"Failed to send login email: {e}")
        messages.error(request, "We couldn't send the login email. Please try again later.")

    return redirect("accounts:login")

def verify_email(request):
    """
    Verify user email address using verification token.

    Args:
        request: Django request object with token in query parameters

    Returns:
        Redirect to login page with success/error message
    """
    token = request.GET.get("token")

    if not token:
        messages.error(request, "Verification token is missing.")
        return redirect("accounts:register")

    data = verify_verification_token(token)

    if not data:
        messages.error(request, "Invalid or expired verification token. Please request a new verification email.")
        return redirect("accounts:register")

    try:
        user = User.objects.get(email=data.email)

        # Check if already verified
        if user.is_verified:
            messages.info(request, "Your email is already verified. You can log in now.")
            return redirect("accounts:login")

        user.is_verified = True
        user.save()
        messages.success(request, "Email verified successfully! You can now log in.")
    except User.DoesNotExist:
        messages.error(request, "User account not found. Please register again.")
        return redirect("accounts:register")
    except Exception as e:
        logger.error(f"Error verifying email: {e}")
        messages.error(request, "An error occurred during verification. Please try again.")
        return redirect("accounts:register")

    return redirect("accounts:login")

def login_confirm(request):
    """
    Confirm login using magic link token.

    Args:
        request: Django request object with token in query parameters

    Returns:
        Redirect to landing page on success, login page on error
    """
    token = request.GET.get("token")

    if not token:
        messages.error(request, "Login token is missing.")
        return redirect("accounts:login")

    data = verify_login_token(token)

    if not data:
        messages.error(request, "Invalid or expired login token. Please request a new login link.")
        return redirect("accounts:login")

    try:
        user = User.objects.get(email=data.email)

        # Check if user is verified (shouldn't happen, but safety check)
        if not user.is_verified:
            messages.warning(request, "Please verify your email address before logging in.")
            return redirect("accounts:login")

        login(request, user)
        messages.success(request, f"Welcome back, {user.name}!")
    except User.DoesNotExist:
        messages.error(request, "User account not found. Please register first.")
        return redirect("accounts:register")
    except Exception as e:
        logger.error(f"Error during login confirmation: {e}")
        messages.error(request, "An error occurred during login. Please try again.")
        return redirect("accounts:login")

    return redirect("core:landing")

def logout_view(request):
    """
    Handle user logout.

    Args:
        request: Django request object

    Returns:
        Redirect to landing page
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("core:landing")

@staff_member_required
def delete_user(request, email):
    """
    Delete a user account (staff only).

    Args:
        request: Django request object
        email: Email address of user to delete

    Returns:
        Redirect to landing page with success/error message
    """
    try:
        user = User.objects.get(email=email)
        user.delete()
        messages.success(request, "User deleted")

    except User.DoesNotExist:
        messages.error(request, "User doesn't exist.")
        return redirect('core:landing')

    except Exception as e:
        messages.error(request, f"Unexpected error: {e}")
        return redirect('core:landing')

    return redirect('core:landing')
