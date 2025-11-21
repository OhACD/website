from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from django.core import signing
from django.utils import timezone

from .models import MagicLink

MAGIC_LINK_SALT = "magic-link"


@dataclass
class TokenPayload:
    email: str
    exp: float
    token_id: str
    token_type: str


def _stamp_payload(email: str, expires: int, token_type: str) -> TokenPayload:
    expires_at = timezone.now() + timedelta(seconds=expires)
    magic_link = MagicLink.objects.create(
        email=email,
        token_type=token_type,
        expires_at=expires_at,
    )
    return TokenPayload(
        email=email,
        exp=expires_at.timestamp(),
        token_id=str(magic_link.id),
        token_type=token_type,
    )


def _generate_token(payload: TokenPayload) -> str:
    return signing.dumps(payload.__dict__, salt=MAGIC_LINK_SALT)


def generate_login_token(email: str, expires: int = 1800) -> str:
    return _generate_token(_stamp_payload(email, expires, MagicLink.TokenType.LOGIN))


def generate_verification_token(email: str, expires: int = 60 * 60 * 24) -> str:
    return _generate_token(_stamp_payload(email, expires, MagicLink.TokenType.VERIFY))


def _verify_token(token: str, max_age: int, token_type: str) -> Optional[TokenPayload]:
    try:
        data = signing.loads(token, salt=MAGIC_LINK_SALT, max_age=max_age)
        payload = TokenPayload(**data)

        if payload.token_type != token_type:
            return None

        magic_link = MagicLink.objects.filter(id=payload.token_id, token_type=token_type).first()
        if not magic_link or magic_link.is_used or magic_link.is_expired:
            return None

        if payload.exp < timezone.now().timestamp():
            return None

        magic_link.mark_used()
        return payload
    except Exception:
        return None


def verify_login_token(token: str, max_age: int = 1800) -> Optional[TokenPayload]:
    return _verify_token(token, max_age, MagicLink.TokenType.LOGIN)


def verify_verification_token(token: str, max_age: int = 60 * 60 * 24) -> Optional[TokenPayload]:
    return _verify_token(token, max_age, MagicLink.TokenType.VERIFY)
