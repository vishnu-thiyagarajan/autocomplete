from django import forms
from .models import currency_convertion
from datetime import date


class CurrencyPredictionForm(forms.ModelForm):
    amount = forms.IntegerField()
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), initial=date.today())
    waiting_time_in_days = forms.IntegerField()

    class Meta:
        model = currency_convertion
        fields = ['base_currency', 'target_currency']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if 0 < amount <= 9999999999:
            return amount
        else:
            raise forms.ValidationError("amount should be positive integer below 10000000000")

    def clean_waiting_time_in_days(self):
        waiting_time = self.cleaned_data.get('waiting_time_in_days')
        if 0 < waiting_time <= 9999999999:
            return waiting_time
        else:
            raise forms.ValidationError("waiting_time should be positive integer below 10000000000")

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if (start_date < date(1999, 3, 4)):
            raise forms.ValidationError("There is no data for dates older then 04/03/1999")
        return start_date
