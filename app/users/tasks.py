from datetime import datetime

from celery.app import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

from users.models import User, BirthdaySubscription


def send_email(subject, body, to):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[to],
    )
    email.send()


@shared_task
def send_notification_to_user(user_id: int):
    user = User.objects.get(id=user_id)
    today = datetime.today().date()
    subscriptions = BirthdaySubscription.objects.filter(
        follower=user,
        subscriber__birthday=today,
    )
    for subscriber in subscriptions:

        send_email(
            "Birthday Reminder",
            f"Today is {subscriber.subscriber.username}'s birthday!",
            subscriber.subscriber.email,
        )
