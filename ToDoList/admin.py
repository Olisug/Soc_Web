from django.contrib import admin

from ToDoList.models import TodoListItem


@admin.register(TodoListItem)
class TodoappListItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'add_time', 'completed')
    fields = ('id',
              'name',
              'author',
              'add_time',
              'completed')
    readonly_fields = ('add_time', 'completed')
    search_fields = ('name',)
    ordering = ('name',)