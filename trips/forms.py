from django import forms

from .models import Terminal


class SearchForm(forms.Form):

    name_from = forms.ModelChoiceField(
        queryset=Terminal.objects.all(),
        label='Hacia',
        widget=forms.Select(attrs={'class': '' })
        )
    name_to = forms.ModelChoiceField(
        queryset=Terminal.objects.all(),
        label='Hacia',
        widget=forms.Select(attrs={'class': '' })
        )
