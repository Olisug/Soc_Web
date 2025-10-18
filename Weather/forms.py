from django import forms


class WeatherForm(forms.Form):
    city = forms.CharField(
        label='Город',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите название города...',
            'class': 'form-control'
        }))