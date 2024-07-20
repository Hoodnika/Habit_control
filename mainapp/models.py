import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from config.settings import AUTH_USER_MODEL
from config.special_elements import NULLABLE


class Place(models.Model):
    place_name = models.CharField(max_length=255, verbose_name='название места')
    address = models.CharField(max_length=300, verbose_name='адрес места', **NULLABLE)
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='создатель места',
        related_name='place'
    )

    def __str__(self):
        return self.place_name

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'


class Habit(models.Model):
    class Periodicity(models.TextChoices):
        per_day = 'раз в день'
        per_half_day = '2 раза в день'
        per_half_week = '2 раза в неделю'
        per_week = 'раз в неделю'

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
        related_name='habit'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.SET_NULL,
        verbose_name='место',
        **NULLABLE
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name='связанная привычка',
        **NULLABLE,
    )
    habit_name = models.CharField(
        max_length=255,
        verbose_name='название привычки'
    )
    time_to_action = models.TimeField(verbose_name='время когда выполнять привычки')
    periodicity = models.CharField(
        choices=Periodicity.choices,
        default=Periodicity.per_day,
        max_length=15,
        verbose_name='частота выполнения привычки'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='признак публичности'
    )
    is_nice = models.BooleanField(
        default=False,
        verbose_name='признак приятной привычки'
    )
    reward = models.CharField(
        max_length=255,
        verbose_name='вознаграждение',
        **NULLABLE
    )
    time_to_complete = models.DurationField(
        verbose_name='время на выполнение привычки',
        validators=[MaxValueValidator(datetime.timedelta(seconds=120))]
    )

    def __str__(self):
        return self.habit_name

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError('Укажите или связанную привычку или вознаграждение')
        if self.is_nice and self.reward:
            raise ValidationError('У приятной привычки не может быть вознаграждения')
        if self.is_nice and self.related_habit:
            raise ValidationError('У приятной привычки не может быть связанной привычки')
        if self.related_habit and not self.related_habit.is_nice:
            raise ValidationError('У связанной привычки должен быть признак приятной.')
