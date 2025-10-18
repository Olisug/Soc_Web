from django.db import models


class Apps(models.Model):
    app_name = models.CharField('Наименование приложения',
                                max_length=100,
                                blank=False)
    emblem = models.CharField('Ярлык',
                              max_length=10,
                              blank=False)
    description = models.TextField('Описание приложения',
                                   max_length=500,
                                   blank=False)
    url = models.CharField('Url-адрес приложения',
                           max_length=1000,
                           blank=False)
    base_url = models.CharField('Url-адрес микросервиса',
                                max_length=1000,
                                blank=True)

    def __str__(self):
        return str(self.app_name)

    class Meta:
        verbose_name = 'Приложение'
        verbose_name_plural = 'Приложения'
