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
                  'city',
                  'birth_date',
                  'email',
                  'short_name',
                  'password1',]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }


# class CustomUserCreationForm(UserCreationForm):
#     city = forms.CharField(
#         widget=CityAutocompleteWidget(attrs={
#             'class': 'form-control city-autocomplete',
#             'placeholder': 'Начните вводить название города...'
#         }),
#         required=False,
#         label='Город'
#     )
    
#     class Meta:
#         model = Profile
#         fields = ['username', 'email', 'password1', 'password2', 'city', 'birth_date']
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Добавляем классы к остальным полям
#         for field_name, field in self.fields.items():
#             if field_name != 'city':  # Город уже настроен
#                 field.widget.attrs.update({'class': 'form-control'})



class UserLoginForm(forms.Form):
    username = forms.CharField(label='Имя')
    password = forms.CharField(label='Пароль')
