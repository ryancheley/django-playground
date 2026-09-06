from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from core.models import Base


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(Base):
    title = models.CharField(max_length=255)
    body = CKEditor5Field()
    published_date = models.DateTimeField(blank=True, null=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = ForeignKey(User, on_delete=models.CASCADE, related_name="author")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Ensure this points to a valid detail route
        return reverse("post-detail", kwargs={"pk": self.pk})
