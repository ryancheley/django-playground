from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

INPUT_CLASSES = (
    "block w-full rounded-md border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
)


class CustomLoginView(LoginView):
    authentication_form = AuthenticationForm
    success_url = reverse_lazy("login")
    template_name = "registration/login.html"
    extra_context = {"title": "Log In"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES
        return form


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    extra_context = {"title": "Signup"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES
        return form
