from django.urls import path
from users.views import (
    CreateUser,
    ListUsers,
    ProfileView,
    Subscribe,
    Unsubscribe,
    UnsubscribeAll,
)

app_name = "users"
urlpatterns = [
    path("", ListUsers.as_view(), name="list"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("registration", CreateUser.as_view(), name="registration"),
    path("subscribe/<int:pk>", Subscribe.as_view(), name="subscribe"),
    path("unsubscribe/<int:pk>", Unsubscribe.as_view(), name="unsubscribe"),
    path("unsubscribe-all", UnsubscribeAll.as_view(), name="unsubscribe_all"),
]
