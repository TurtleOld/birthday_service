from django.contrib.auth.forms import UserCreationForm
from django.forms import (
    Form,
    DateInput,
    ChoiceField,
)

from users.models import User


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "birthday",
            "password1",
            "password2",
        ]
        widgets = {
            "birthday": DateInput(attrs={"type": "date"}),
        }


class NotificationTimeForm(Form):
    TIME_CHOICES = [
        (15, "15 минут"),
        (30, "30 минут"),
        (60, "1 час"),
        (120, "2 часа"),
        (180, "3 часа"),
    ]
    notification_time = ChoiceField(choices=TIME_CHOICES, label="Уведомить за")
