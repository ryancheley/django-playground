from django import forms

SEASON_CHOICES = [
    ("R", "Regular"),
    ("P", "Post"),
    ("A", "All Star"),
]


class SeasonForm(forms.Form):
    season_type = forms.ChoiceField(choices=SEASON_CHOICES)
