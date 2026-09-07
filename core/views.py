from django.contrib.auth.mixins import LoginRequiredMixin
from neapolitan.views import CRUDView

from .models import UserProfile


class UserProfileView(LoginRequiredMixin, CRUDView):
    model = UserProfile
    fields = ["bio"]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.user = user
        self.object.created_by = user
        self.object.modified_by = user

        form.save_m2m()

        self.object.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = getattr(self, "object", None)
        context["title"] = user if user else "User Profile"
        return context
