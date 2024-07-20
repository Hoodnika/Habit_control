from rest_framework.serializers import ValidationError

from mainapp.models import Habit


class NoRewardWithRelated:
    """
    Валидация на отсутствие вознаграждения и связанной привычки одновременно
    """

    def __call__(self, habit):
        if habit.get('related_habit') and habit.get('reward'):
            raise ValidationError('Укажите или связанную привычку или вознаграждение')


class NoRewardIfNice:
    """
    Валидация на отсутствие вознаграждения при приятной привычке
    """

    def __call__(self, habit):
        if habit.get('is_nice') and habit.get('reward'):
            raise ValidationError('У приятной привычки не может быть вознаграждения')


class NoRelatedIfNice:
    """
    Валидация на отсутствие связанной привычки при приятной привычке
    """

    def __call__(self, habit):
        if habit.get('is_nice') and habit.get('related_habit'):
            raise ValidationError('У приятной привычки не может быть связанной привычки')


class RelatedMustBeNice:
    """
    Валидация на признак приятной связанной привычки
    """

    def __call__(self, habit):
        related_name = habit.get('related_habit')
        if related_name:
            related_habit = Habit.objects.get(habit_name=related_name)
            if not related_habit.is_nice:
                raise ValidationError('У связанной привычки должен быть признак приятной.')


