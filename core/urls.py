from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from health_check.views import HealthCheckView

from core.settings import DEBUG_TOOLBAR

from .views import UserProfileView

urlpatterns = [
    path("", views.flatpage, kwargs={"url": "/"}, name="home"),
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="health_check"),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("blog/", include("blog.urls")),
    *UserProfileView.get_urls(),
]

if DEBUG_TOOLBAR:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
