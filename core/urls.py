from core.settings import DEBUG
from django.contrib import admin
from django.urls import include, path

from debug_toolbar.toolbar import debug_toolbar_urls
from health_check.views import HealthCheckView

urlpatterns = [
    path('/', include("django.contrib.flatpages.urls")),
    path('admin/', admin.site.urls),
    path('health/', HealthCheckView.as_view(), name='health_check'),
]

if DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]