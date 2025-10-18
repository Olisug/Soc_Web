from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TodoListItem(models.Model):
    name = models.CharField('Наименование задачи', max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                               blank=True)
    add_time = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=True)
    completed = models.BooleanField('Стадия выполнения',
                                    default=False,
                                    help_text='Нажмите галочку, чтобы'
                                    'завершить задачу')

    def __str__(self):
        if self.completed is True:
            return f'Задача {self.name}, автор {self.author.username} - выполнена.'
        elif self.completed is False:
            return f'Задача {self.name}, автор {self.author.username}.'