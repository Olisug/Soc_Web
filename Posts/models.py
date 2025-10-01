from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Posts(models.Model):
    text = models.CharField('Текст статьи',
                            max_length=1000)
    photo = models.FileField('Фото',
                             upload_to='media/images/post',
                             blank=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               verbose_name='Автор поста')
    pub_time = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=True)

    def __str__(self):
        text = str(self.text)
        return f"{text[:15]}..." if len(text) > 10 else text

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Likes(models.Model):
    maker = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True,
                              verbose_name='Автор')
    for_post = models.ForeignKey(Posts,
                                 on_delete = models.CASCADE,
                                 verbose_name='Публикация')

    def __str__(self):
        text = str(self.for_post.text)
        return f"{text[:10]}..." if len(text) > 10 else text

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'