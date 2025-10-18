from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import TodoListItem
from ToDoList.forms import TodoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class TodoListItemList(LoginRequiredMixin, ListView):
    model = TodoListItem
    template_name = 'todoapp/tasks.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        return TodoListItem.objects.filter(author=self.request.user).order_by('id')


class CreateTask(LoginRequiredMixin, CreateView):
    model = TodoListItem
    form_class = TodoForm
    template_name = 'todoapp/create.html'
    success_url = reverse_lazy('ToDoList:tasks')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditTask(LoginRequiredMixin, UpdateView):
    model = TodoListItem
    form_class = TodoForm
    template_name = 'todoapp/edit.html'
    success_url = reverse_lazy('ToDoList:tasks')

    def get_queryset(self):
        return TodoListItem.objects.filter(author=self.request.user)


@login_required
def delete_task(request, id):
    item = get_object_or_404(TodoListItem, id=id, author=request.user)
    item.delete()
    return redirect('ToDoList:tasks')


@login_required
def complete_task(request, id):
    item = TodoListItem.objects.get(id=id, author=request.user)
    item.completed = True
    item.save()
    return redirect('ToDoList:tasks')