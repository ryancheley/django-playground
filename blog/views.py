from django.contrib.auth.mixins import LoginRequiredMixin
from neapolitan.views import CRUDView

from .forms import PostForm
from .models import Post


class PostView(LoginRequiredMixin, CRUDView):
    model = Post
    fields = ["title", "body", "published_date", "categories", "slug"]
    form_class = PostForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        form.instance.created_by = user
        form.instance.modified_by = user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = getattr(self, "object", None)
        context["title"] = post.title if post else "Posts"
        return context
