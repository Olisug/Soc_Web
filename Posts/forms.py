from django import forms
from .models import Posts

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Posts
#         fields = ['text', 'photo']  # Явно указываем поля
#         widgets = {
#             'text': forms.Textarea(attrs={
#                 'placeholder': 'Текст статьи',
#                 'rows': 5,
#                 'class': 'post-textarea'
#             }),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['text'].required = True
#         self.fields['photo'].required = False


class PostForm(forms.ModelForm):

    class Meta:
        model = Posts
        exclude = ('author', 'pub_time')
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Текст статьи',
                'rows': 5,
                'class': 'post-textarea'
            }),
        }

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        return photo