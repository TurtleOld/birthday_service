from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy

from users.models import User, BirthdaySubscription

from users.forms import RegisterUserForm, NotificationTimeForm
from users.tasks import send_notification_to_user


class IndexView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("birthday:list")
        return redirect("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = NotificationTimeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = NotificationTimeForm(request.POST)
        if form.is_valid():
            notification_time_minutes = int(form.cleaned_data["notification_time"])
            subscription_exists = BirthdaySubscription.objects.filter(
                follower=self.request.user,
            )
            for subscription in subscription_exists:
                birthday = subscription.subscriber.birthday
                notification_time = birthday - timezone.timedelta(
                    minutes=notification_time_minutes
                )
                send_notification_to_user.apply_async(
                    (subscription.id,), eta=notification_time
                )
            return redirect("users:profile")
        return render(request, self.template_name, {"form": form})


class ListUsers(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    model = User
    template_name = "users/list.html"
    context_object_name = "users"
    no_permission_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["users"] = User.objects.exclude(id=self.request.user.id)

        return context


class LoginUser(SuccessMessageMixin, LoginView):
    model = User
    template_name = "users/login.html"
    next_page = "/"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_login_form"] = self.form_class
        return context

    def form_invalid(self, form):
        messages.error(
            self.request,
            form.errors["__all__"][0],
        )
        return super().form_invalid(form)


class LogoutUser(SuccessMessageMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(
            request,
            messages.SUCCESS,
            "Your account has been logged out.",
        )
        return super().dispatch(request, *args, **kwargs)


class CreateUser(SuccessMessageMixin, CreateView):
    model = User
    template_name = "users/registration.html"
    form_class = RegisterUserForm
    success_message = "Registration was successful!"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registration form"
        context["button_text"] = "Registration"
        return context


class Subscribe(CreateView):
    template_name = "users/list.html"
    model = BirthdaySubscription

    def get(self, request, *args, **kwargs):
        user_subscribe = get_object_or_404(User, id=kwargs["pk"])
        subscription_exists = BirthdaySubscription.objects.filter(
            subscriber=user_subscribe,
            follower=request.user,
        ).exists()

        if subscription_exists:
            messages.error(request, "You are already subscribed to this user.")
        else:
            BirthdaySubscription.objects.create(
                subscriber=user_subscribe,
                follower=request.user,
            )
            messages.success(request, "Subscription successful.")

        return redirect("users:list")


class Unsubscribe(UpdateView):
    template_name = "subscription.html"
    model = BirthdaySubscription

    def get(self, request, *args, **kwargs):
        user_subscribe = get_object_or_404(User, id=kwargs["pk"])
        subscription_exists = BirthdaySubscription.objects.filter(
            subscriber=user_subscribe,
            follower=request.user,
        )

        if subscription_exists.exists():
            subscription_exists.delete()
            messages.success(request, "Unsubscription successful.")

        return redirect("birthday:subscription")


class UnsubscribeAll(UpdateView):
    template_name = "subscription.html"
    model = BirthdaySubscription

    def get(self, request, *args, **kwargs):
        BirthdaySubscription.objects.filter(
            follower=request.user,
        ).delete()

        messages.success(request, "Unsubscription successful.")

        return redirect("birthday:subscription")
