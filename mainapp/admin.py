from django.contrib import admin

from mainapp.models import Habit, Place


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('pk', 'habit_name', 'time_to_action', 'periodicity', 'is_public', 'is_nice', 'reward', 'time_to_complete', 'related_habit', 'user', 'place')
    list_filter = ('is_public', 'is_nice', 'periodicity', 'user', 'place')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'place_name', 'user')
