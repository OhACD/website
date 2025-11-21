import asyncio
import os
from functools import partial

from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.urls import reverse

from .tokens import generate_login_token, generate_verification_token

SENDER_EMAIL = os.getenv("EMAIL_HOST_USER")


def _build_magic_link(request, url_name, token):
    return request.build_absolute_uri(f"{reverse(url_name)}?token={token}")


async def _send_mail_async(*args, **kwargs):
    loop = asyncio.get_event_loop()
    send = partial(send_mail, *args, **kwargs)
    await loop.run_in_executor(None, send)


def send_verification_email(request, email):
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
