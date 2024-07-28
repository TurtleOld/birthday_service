from django.urls import path

from birthday_app.views import BirthdayTemplateView, Subscription

app_name = "birthday"
urlpatterns = [
    path("", BirthdayTemplateView.as_view(), name="list"),
    path("subscription/", Subscription.as_view(), name="subscription"),
]
