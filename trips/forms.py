from django import forms

from .models import Terminal


class SearchForm(forms.Form):
    name_from = forms.ModelChoiceField(
        queryset=Terminal.objects.all(),
        label="Hacia",
        widget=forms.Select(attrs={"name": "name_from"}),
    )
    name_to = forms.ModelChoiceField(
        queryset=Terminal.objects.all(),
        label="Hacia",
        widget=forms.Select(attrs={"name": "name_to"}),
    )
