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


class ActiveNavigationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Navigation(Base):
    title = models.CharField(max_length=100, unique=True)
    uri_path = models.CharField(max_length=255)
    active = models.BooleanField(null=True)

    # The order below is important per [Default Managers](https://docs.djangoproject.com/en/6.1/topics/db/managers/#default-managers)
    objects = models.Manager()
    active_objects = ActiveNavigationManager()

    def __str__(self):
        return str(self.title)
