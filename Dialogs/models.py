from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User,
                               on_delete=models.DO_NOTHING,
                               verbose_name='Отправитель')
    reciever = models.ForeignKey(User,
                                 related_name='to_reciever',
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='Получатель')
    message_text = models.TextField('Текст сообщения')
    message_image = models.ImageField('Изображение',
                                      blank=True,
                                      upload_to='images/messages/')
    message_time = models.DateTimeField('Время отправления')
    is_readed = models.BooleanField('Прочитано',
                                    default=False)
    sender_visibility = models.BooleanField('Отображение у отправителя',
                                            default=True)
    reciever_visibility = models.BooleanField('Отображение у получателя',
                                              default=True)

    def __str__(self):
        return f'Cообщение от пользователя {str(self.sender)} пользователю {str(self.reciever)}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
