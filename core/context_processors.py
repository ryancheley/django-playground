from blog.models import Post


def stupid_context(request):
    post_count = Post.objects.all().count()
    return {"stupid": post_count}
