from django.contrib.auth.models import User
from django.db import models


class Base(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_created",
        related_query_name="%(app_label)s_%(class)s_created",
    )
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_modified",
        related_query_name="%(app_label)s_%(class)s_modified",
    )
    modify_timestamp = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class UserProfile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)

    def __str__(self):
        return str(self.user)


class Navigation(Base):
    title = models.CharField(max_length=100, unique=True)
    uri_path = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)
