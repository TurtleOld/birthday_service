from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    birthday = models.DateField(blank=True, null=True)
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True,
        related_query_name="user",
    )

    def __str__(self):
        return self.username


class BirthdaySubscription(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="subscribers",
        on_delete=models.CASCADE,
    )
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followers",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("subscriber", "follower")

    def __str__(self):
        return f"{self.follower} subscribed to {self.subscriber}"
