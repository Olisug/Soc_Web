import requests
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta, timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class CityField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 100)
        kwargs.setdefault('blank', True)
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value and not self.is_valid_city(value):
            raise ValidationError(f'Город "{value}" не найден в базе данных')

    def is_valid_city(self, city_name):
        """Проверяет, существует ли город в базе Oxilor"""
        try:
            url = "https://data.oxilor.com/rest/regions"
            params = {
                "name": city_name,
                "language": "ru",
                "types": "city"
            }
            headers = {
                "Authorization": "Bearer objkpuDQEy6GCdX2iArwrXnRB19wPs"
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return any(city['name'].lower() == city_name.lower() for city in data.get('data', []))
            return False
        except:
            return False  # При ошибке сети считаем город валидным


class Profile(AbstractUser):
    '''Оформляет аккаунт пользователя'''
    GENDER_CHOICE = (("M", "М"),
                     ("F", "Ж"),
                     (None, "-"))
    avatar = models.ImageField('Аватар',
                               blank=True,
                               upload_to='images/avatar/')
    gender = models.CharField('Пол',
                              max_length=1,
                              choices=GENDER_CHOICE,
                              blank=True)
    # city = models.CharField('Город',
    #                         max_length=100,
    #                         blank=True)
    city = CityField('Город')
    birth_date = models.DateField('Дата рождения',
                                  null=True,
                                  blank=True)
    email = models.CharField('Почтовый адрес', max_length=20,
                             null=False,
                             blank=False)
    short_name = models.CharField('Короткое имя',
                                  max_length=10,
                                  null=True,
                                  blank=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @staticmethod
    def get_cities_suggestions(query):
        """Получает список городов из API Oxilor"""
        try:
            url = "https://data.oxilor.com/rest/regions"
            params = {
                "name": query,
                "language": "ru",
                "types": "city",
                "limit": 10
            }
            headers = {
                "Authorization": "Bearer objkpuDQEy6GCdX2iArwrXnRB19wPs"
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                cities = [city['name'] for city in data.get('data', [])]
                return cities
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Ошибка при получении городов: {e}")
            return []


class Status(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    online = models.DateTimeField('Был в онлайне',
                                  null=True,
                                  blank=True)

    def __str__(self):
        return str(self.user)

    def get_online_status(self):
        status = ''
        timezone_delta = timedelta(hours=3, minutes=0)
        online_status_true = timedelta(minutes=5)
        user_online = self.online + timezone_delta
        if self.profile.gender == 'F':
            if user_online.date() == (datetime.now()-timedelta(days=1)).date():
                status = 'Была онлайн вчера в '+user_online.time().strftime(
                    "%H:%M")
            elif timezone.now()-self.online < online_status_true:
                status = 'Онлайн'
            elif user_online.date() == datetime.now().date():
                status = 'Была онлайн сегодня в '+user_online.time().strftime(
                    "%H:%M")
            elif user_online.date().year == datetime.now().date().year:
                status = 'Была онлайн '+user_online.date().strftime(
                    "%d.%m")+' в '+user_online.time().strftime("%H:%M")
            else:
                status = 'Была онлайн '+user_online.date().strftime(
                    "%d.%m.%Y")+' в '+user_online.time().strftime("%H:%M")
        else:
            if user_online.date() == (datetime.now()-timedelta(days=1)).date():
                status = 'Был онлайн вчера в '+user_online.time().strftime(
                    "%H:%M")
            elif timezone.now()-self.online < online_status_true:
                status = 'Онлайн'
            elif user_online.date() == datetime.now().date():
                status = 'Был онлайн сегодня в '+user_online.time().strftime(
                    "%H:%M")
            elif user_online.date().year == datetime.now().date().year:
                status = 'Был онлайн '+user_online.date().strftime(
                    "%d.%m")+' в '+user_online.time().strftime("%H:%M")
            else:
                status = 'Был онлайн '+user_online.date().strftime(
                    "%d.%m.%Y")+' в '+user_online.time().strftime("%H:%M")
        return status

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Friend(models.Model):
    user = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    users_friend = models.ForeignKey(Profile,
                                     related_name='users_friend',
                                     on_delete=models.CASCADE,
                                     verbose_name='В дружбе с ...')
    confirmed = models.BooleanField('Подтверждено',
                                    default=False)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'


User = get_user_model()


class Follower(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    follower_for = models.ForeignKey(User,
                                     related_name='follower_for',
                                     on_delete=models.CASCADE,
                                     verbose_name='Подписан на ...')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
