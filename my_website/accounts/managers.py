from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user manager for the User model.
    Handles user creation with email as the primary identifier.
    """

    def create_user(self, email, name, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and name.

        Args:
            email: User's email address (required)
            name: User's full name (required)
            password: Optional password (not used in passwordless auth)
            **extra_fields: Additional user fields

        Returns:
            User instance

        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError("Users must have a valid email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Create and return a superuser with the given email, name, and password.

        Args:
            email: User's email address
            name: User's full name
            password: Password for superuser (required)
            **extra_fields: Additional user fields

        Returns:
            User instance with superuser privileges

        Raises:
            ValueError: If password is not provided
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Superusers must have a password.")

        return self.create_user(email, name, password=password, **extra_fields)
