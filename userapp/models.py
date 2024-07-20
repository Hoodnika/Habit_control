from django.contrib.auth.models import AbstractUser
from django.db import models

from config.special_elements import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта', help_text='обязательное поле', **NULLABLE)
    phone = models.CharField(max_length=40, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=60, verbose_name='страна', **NULLABLE)
    last_login = models.DateTimeField(auto_now=True, verbose_name='заходил в последний раз', **NULLABLE)
    tg_username = models.CharField(unique=True, max_length=100, verbose_name='имя пользователя в телеграме')
    tg_id = models.CharField(unique=True, max_length=50, verbose_name='id телеграма', **NULLABLE, help_text='Введите id, чтобы получать оповещения в телеграме')

    USERNAME_FIELD = 'tg_username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.tg_username

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
