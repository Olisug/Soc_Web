from django.urls import path

from ToDoList import views

app_name = 'ToDoList'

urlpatterns = [
    path('tasks/', views.TodoListItemList.as_view(), name='tasks'),
    path('create/', views.CreateTask.as_view(), name='create'),
    path('edit/<int:pk>', views.EditTask.as_view(), name='edit'),
    path('delete/<int:id>', views.delete_task, name='delete'),
    path('complete/<int:id>', views.complete_task, name='complete'),
]