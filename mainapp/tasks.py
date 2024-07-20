import time
from datetime import timedelta, datetime, date

from celery import shared_task
from celery.signals import worker_ready
from django.core.cache import cache
from django.utils import timezone

from mainapp.models import Habit
from mainapp.services import send_telegram_notice


@shared_task()
def redis_clear_and_get():
    habits_to_cache = []
    habits = Habit.objects.all()
    for habit in habits:
        if not habit.is_nice and habit.user.tg_id:
            time_to_comparison = timezone.make_aware(datetime.combine(date.today(), habit.time_to_action))
            if timedelta(seconds=0) < time_to_comparison - timezone.now() <= timedelta(hours=2):
                habits_to_cache.append(habit)
    cache.set('habits_to_cache', habits_to_cache, 7205)

@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    redis_clear_and_get.delay()  # запускаем кеширование сразу при запуске воркера

@shared_task()
def send_notice_habit_telegram():
    habits_to_cache = cache.get('habits_to_cache')
    if habits_to_cache:
        for habit in habits_to_cache:

            if not habit.place:
                place = 'где-нибудь'
            else:
                place = habit.place.place_name

            if habit.reward:
                reward = f'получишь {habit.reward}'
            else:
                reward = f'можешь {habit.related_habit.habit_name}'

            if habit.time_to_action.hour * 60 + habit.time_to_action.minute == timezone.now().hour * 60 + timezone.now().minute:
                # сравниваем кол-во минут, потому если просто habit.time_to_action == timezone.now(), то условие никогда не сработает из-за миллисекунд
                if habit.periodicity == Habit.Periodicity.per_day:
                    message = f'Опа, сейчас {habit.time_to_action}, а значит пора {habit.habit_name} находясь {place}!\nА за это ты {reward}'
                    send_telegram_notice(message, habit.user.tg_id)

                if habit.periodicity == Habit.Periodicity.per_half_day:
                    message = f'Опа, сейчас {timezone.now().time()}, а значит пора {habit.habit_name} находясь {place}!\nА за это ты {reward}'
                    send_telegram_notice(message, habit.user.tg_id)
                    time.sleep(14400)
                    # Дал функции уснуть на 4 часа, для повторной отправки, хз, насколько это правильная практика, если ты наставник, который читает это
                    # то дай какой-нибудь комментарий насчет этого
                    message = f'Опа, сейчас {timezone.now().time()}, а значит пора {habit.habit_name} находясь {place}!\nА за это ты {reward}'
                    send_telegram_notice(message, habit.user.tg_id)
                if habit.periodicity == Habit.Periodicity.per_week:
                    if timezone.now().weekday() == 0:  # Пусть пользователь начинают новую неделю с повторением привычки
                        message = f'С понедельником, знаю, это нелегкий день, но уже {habit.time_to_action} и тебе нужно {habit.habit_name} находясь {place}!\nА за это ты {reward}'
                        send_telegram_notice(message, habit.user.tg_id)
                if habit.periodicity == Habit.Periodicity.per_half_week:
                    if timezone.now().weekday() in [0, 4]:
                        message = f'Не, ну ты время-то видел вообще? Сейчас же {habit.time_to_action}, а значит тебе нужно {habit.habit_name} находясь {place}!\nА за это ты {reward}'
                        send_telegram_notice(message, habit.user.tg_id)

