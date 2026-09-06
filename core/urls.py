from core.settings import DEBUG
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

from debug_toolbar.toolbar import debug_toolbar_urls
from health_check.views import HealthCheckView

from .views import UserProfileView

urlpatterns = [
    path("", views.flatpage, kwargs={"url": "/"}, name="home"),
    path('admin/', admin.site.urls),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    *UserProfileView.get_urls(),
]

if DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]