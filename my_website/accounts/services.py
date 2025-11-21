"""
Email service functions for sending magic link emails.

This module handles asynchronous email sending for verification and login links.
"""

import asyncio
import os
from functools import partial

from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.urls import reverse

from .tokens import generate_login_token, generate_verification_token

SENDER_EMAIL = os.getenv("EMAIL_HOST_USER")


def _build_magic_link(request, url_name, token):
    """
    Build absolute URL for magic link.

    Args:
        request: Django request object
        url_name: URL name pattern
        token: Authentication token

    Returns:
        Absolute URL string
    """
    return request.build_absolute_uri(f"{reverse(url_name)}?token={token}")


async def _send_mail_async(*args, **kwargs):
    """
    Send email asynchronously in a thread pool.

    Args:
        *args: Positional arguments for send_mail
        **kwargs: Keyword arguments for send_mail
    """
    loop = asyncio.get_event_loop()
    send = partial(send_mail, *args, **kwargs)
    await loop.run_in_executor(None, send)


def send_verification_email(request, email):
    """
    Send email verification link to user.

    Args:
        request: Django request object
        email: Recipient email address

    Returns:
        Verification URL string

    Raises:
        Exception: If email sending fails
    """
    token = generate_verification_token(email)
    url = _build_magic_link(request, "accounts:verify", token)
    async_to_sync(_send_mail_async)(
        "Verify your account",
        f"Click to verify your email:\n\n{url}",
        SENDER_EMAIL,
        [email],
        fail_silently=False,
    )
    return url


def send_login_email(request, email):
    """
    Send magic login link to user.

    Args:
        request: Django request object
        email: Recipient email address

    Returns:
        Login URL string

    Raises:
        Exception: If email sending fails
    """
    token = generate_login_token(email)
    url = _build_magic_link(request, "accounts:login_confirm", token)
    async_to_sync(_send_mail_async)(
        "Your login link",
        f"Click here to log in:\n\n{url}",
        SENDER_EMAIL,
        [email],
        fail_silently=False,
    )
    return url
