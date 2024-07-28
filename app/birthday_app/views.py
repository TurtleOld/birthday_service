from django.views.generic import TemplateView

from users.models import BirthdaySubscription


class BirthdayTemplateView(TemplateView):
    template_name = "home.html"


class Subscription(TemplateView):
    template_name = "subscription.html"
    model = BirthdaySubscription

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subscribers = BirthdaySubscription.objects.filter(
            follower=self.request.user,
        )

        context["subscribers"] = subscribers

        return context
