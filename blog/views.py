from django.contrib.auth.mixins import LoginRequiredMixin
from neapolitan.views import CRUDView

from .forms import PostForm
from .models import Post


class PostView(LoginRequiredMixin, CRUDView):
    model = Post
    fields = ["title", "body", "published_date", "categories", "slug"]
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.author = user
        self.object.created_by = user
        self.object.modified_by = user

        self.object.save()

        return super().form_valid(form)
