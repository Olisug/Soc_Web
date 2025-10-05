from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username',
                  'avatar',
                  'gender',
                  'country',
                  'city',
                  'birth_date',
                  'email',
                  'short_name',
                  'password1',]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }


class UserEditForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['avatar',
                  'gender',
                  'country',
                  'city',
                  'birth_date',
                  'email',
                  'short_name',
                  'password1',]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя')
    password = forms.CharField(label='Пароль')
