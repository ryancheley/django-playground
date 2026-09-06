from neapolitan.views import CRUDView
from .models import UserProfile


class UserProfileView(CRUDView):
    model = UserProfile
    fields = ["bio"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.user = user
        self.object.created_by = user
        self.object.modified_by = user

        self.object.save()

        return super().form_valid(form)