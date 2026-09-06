from django.contrib.auth.models import User
from django.db import models


class Base(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    create_timestamp = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="modified")
    modify_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True)

    def __str__(self):
        return str(self.user)
