from django import forms
from .models import AutoComplete


class AutoCompleteForm(forms.ModelForm):

    class Meta:
        model = AutoComplete
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text:
            return ''
        else:
            raise forms.ValidationError("text should have some value")
