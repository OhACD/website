"""
User models for the accounts app.

This module defines the custom User model and MagicLink model for
passwordless authentication.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using email as the primary identifier.

    This model implements passwordless authentication where users
    authenticate via magic links sent to their email.
    """
    email = models.EmailField(unique=True, help_text="User's email address (used for login)")
    name = models.CharField(max_length=255, help_text="User's full name")
    is_verified = models.BooleanField(default=False, help_text="Whether email has been verified")
    mailing_list = models.BooleanField(default=False, help_text="Opt-in for mailing list")
    is_staff = models.BooleanField(default=False, help_text="Staff status")
    date_joined = models.DateTimeField(default=timezone.now, help_text="Account creation date")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email


class MagicLink(models.Model):
    """
    Model for tracking magic link tokens.

    Each token can only be used once and expires after a set time period.
    """
    class TokenType(models.TextChoices):
        """Types of magic link tokens."""
        LOGIN = "login", "Login"
        VERIFY = "verify", "Verify"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(help_text="Email address associated with this token")
    token_type = models.CharField(max_length=10, choices=TokenType.choices, help_text="Type of token")
    expires_at = models.DateTimeField(help_text="Token expiration timestamp")
    used_at = models.DateTimeField(null=True, blank=True, help_text="When token was used (null if unused)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Token creation timestamp")

    def mark_used(self):
        """Mark this token as used."""
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])

    @property
    def is_expired(self):
        """Check if token has expired."""
        return timezone.now() >= self.expires_at

    @property
    def is_used(self):
        """Check if token has been used."""
        return self.used_at is not None

    def __str__(self):
        return f"{self.token_type} magic link for {self.email}"
