from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from neapolitan.views import CRUDView
from .models import UserProfile


class UserProfileView(LoginRequiredMixin, CRUDView):
    model  = UserProfile
    fields = ["bio"]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.user = user
        self.object.created_by = user
        self.object.modified_by = user

        self.object.save()

        return super().form_valid(form)
