from django import forms

_INPUT = "mt-1 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"


class ContactForm(forms.Form):
    email_address = forms.EmailField(widget=forms.TextInput(attrs={"class": _INPUT}))
    subject = forms.CharField(widget=forms.TextInput(attrs={"class": _INPUT}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": _INPUT, "rows": 4}))
    date_need_response = forms.DateField(
        widget=forms.DateInput(attrs={"class": _INPUT, "type": "date"}, format="%Y-%m-%d")
    )
