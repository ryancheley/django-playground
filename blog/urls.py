from blog.views import PostView

urlpatterns = [
    *PostView.get_urls(),
]
