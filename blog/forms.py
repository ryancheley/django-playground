from django import forms

from .models import Post

_INPUT = "mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "published_date",
            "categories",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": _INPUT}),
            "body": forms.Textarea(attrs={"class": _INPUT, "rows": 4}),
            "published_date": forms.DateInput(attrs={"class": _INPUT, "type": "date"}, format="%Y-%m-%d"),
            "categories": forms.SelectMultiple(attrs={"class": _INPUT}),
        }
