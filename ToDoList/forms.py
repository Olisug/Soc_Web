from django import forms
from .models import TodoListItem


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoListItem
        exclude = ('completed', 'author')


class CompleteTask(forms.ModelForm):
    class Meta:
        model = TodoListItem
        fields = ('completed',)