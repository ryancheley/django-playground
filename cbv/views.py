from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    RedirectView,
    TemplateView,
    UpdateView,
)

from hockey.models import TeamSeason

from .forms import ContactForm, PersonForm
from .models import Person

PersonModelFormset = modelformset_factory(
    Person,
    form=PersonForm,
    extra=1,
    can_delete=True,
    fields=(
        "given_name",
        "surname",
        "date_of_birth",
    ),
)


class MyTemplateView(TemplateView):
    template_name = "cbv/template-view.html"
    extra_context = {
        "title": "Template View Example",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the data and remove it from the session so it doesn't persist forever
        context["message"] = self.request.session.pop("redirect_message", None)
        if context["message"]:
            context["title"] = "Redirect View"
        return context


class MyRedirectView(RedirectView):
    permanent = False
    url = reverse_lazy("template-view")

    def get_redirect_url(self, *args, **kwargs):
        self.request.session["redirect_message"] = "You have been redirected from the redirect page succesfully!"
        return super().get_redirect_url(*args, **kwargs)


class MyDetailView(DetailView):
    queryset = TeamSeason.objects.all()
    template_name = "cbv/detail.html"
    extra_context = {"title": "Team Season Detail View"}


class MyListView(ListView):
    model = TeamSeason
    template_name = "cbv/list.html"
    extra_context = {"title": "Team Season List View"}
    paginate_by = 25


class MyCreateView(LoginRequiredMixin, CreateView):
    model = Person
    fields = ["given_name", "surname", "date_of_birth"]
    extra_context = {"title": "Create a new person"}
    action = "Create"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        return super().form_valid(form)


class MyPersonDetailView(DetailView):
    model = Person
    template_name = "cbv/person-detail.html"
    extra_context = {"title": "Person Detail View"}


class MyPersonUpdateView(UpdateView):
    model = Person
    fields = ["given_name", "surname", "date_of_birth"]
    extra_context = {"title": "Update person"}
    action = "Edit"


class MyPersonDeleteView(DeleteView):
    model = Person
    fields = ["given_name", "surname", "date_of_birth"]
    extra_context = {"title": "Delete person"}
    success_url = reverse_lazy("person-list-view")


class MyPersonListView(ListView):
    model = Person
    template_name = "cbv/person-list.html"
    extra_context = {"title": "Person List View"}
    paginate_by = 10


class MyContactForm(FormView):
    extra_context = {
        "title": "Contact Form View",
    }
    form_class = ContactForm
    template_name = "cbv/contact.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data["email_address"]
        subject = form.cleaned_data["subject"]
        description = form.cleaned_data["description"]
        date_need_response = form.cleaned_data["date_need_response"]

        full_message = (
            f"Message received from {email} \n"
            f"___________________________\n\n"
            f"{subject}\n"
            f"{description}\n"
            f"Responde needed by {date_need_response}"
        )

        send_mail(
            subject=f"[Received Form] {subject}",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL],
        )
        return super().form_valid(form)


class PersonFormSet(FormView):
    form_class = PersonModelFormset
    extra_context = {
        "title": "Person Form Set",
    }
    template_name = "cbv/person-formset.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
