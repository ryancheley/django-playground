from django.urls import path

from .views import (
    MyContactForm,
    MyCreateView,
    MyDetailView,
    MyListView,
    MyPersonDeleteView,
    MyPersonDetailView,
    MyPersonListView,
    MyPersonUpdateView,
    MyRedirectView,
    MyTemplateView,
)

urlpatterns = [
    path("template-view", MyTemplateView.as_view(), name="template-view"),
    path("redirect-view", MyRedirectView.as_view(), name="redirect-view"),
    path("list-view", MyListView.as_view(), name="list-view"),
    path("detail-view/<int:pk>", MyDetailView.as_view(), name="detail-view"),
    path("create-view", MyCreateView.as_view(), name="create-view"),
    path("contact-form", MyContactForm.as_view(), name="contact-form"),
    path("person-list-view", MyPersonListView.as_view(), name="person-list-view"),
    path("person-view/<int:pk>", MyPersonDetailView.as_view(), name="person-view"),
    path("person-update-view/<int:pk>", MyPersonUpdateView.as_view(), name="person-update-view"),
    path("person-delete-view/<int:pk>", MyPersonDeleteView.as_view(), name="person-delete-view"),
]
