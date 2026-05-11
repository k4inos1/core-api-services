from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Centralized Custom User model for the IAM Core API.
    Used by all other apps in the ecosystem to validate identities.
    """

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        CLIENT = "CLIENT", "Client"
        OPERATOR = "OPERATOR", "Operator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
        help_text="Role of the user in the ecosystem",
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
