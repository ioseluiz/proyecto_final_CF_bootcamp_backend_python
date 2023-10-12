from django import forms

from .models import Terminal


class SearchForm(forms.Form):

    name_from = forms.ModelChoiceField(
        queryset=Terminal.objects.all(),
        label='Hacia',
        widget=forms.Select(attrs={'class': 'form-control mb-2 mr-sm-2' })
        )
    name_to = forms.ModelChoiceField(
        queryset=Terminal.objects.all(),
        label='Hacia',
        widget=forms.Select(attrs={'class': 'form-control mb-2 mr-sm-2' })
        )
