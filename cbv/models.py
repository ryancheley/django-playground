from django.db import models
from django.urls import reverse

from core.models import Base


class Person(Base):
    given_name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    date_of_birth = models.DateField()

    def __str__(self):
        return f"{self.given_name} {self.surname} ({self.date_of_birth})"

    def get_absolute_url(self):
        return reverse("person-view", kwargs={"pk": self.pk})
