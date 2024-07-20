# Generated by Django 5.0.6 on 2024-07-20 12:25

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.CharField(max_length=255, verbose_name='название места')),
                ('address', models.CharField(blank=True, max_length=300, null=True, verbose_name='адрес места')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='place', to=settings.AUTH_USER_MODEL, verbose_name='создатель места')),
            ],
            options={
                'verbose_name': 'место',
                'verbose_name_plural': 'места',
            },
        ),
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habit_name', models.CharField(max_length=255, verbose_name='название привычки')),
                ('time_to_action', models.TimeField(verbose_name='время когда выполнять привычки')),
                ('periodicity', models.CharField(choices=[('раз в день', 'Per Day'), ('2 раза в день', 'Per Half Day'), ('2 раза в неделю', 'Per Half Week'), ('раз в неделю', 'Per Week')], default='раз в день', max_length=15, verbose_name='частота выполнения привычки')),
                ('is_public', models.BooleanField(default=False, verbose_name='признак публичности')),
                ('is_nice', models.BooleanField(default=False, verbose_name='признак приятной привычки')),
                ('reward', models.CharField(blank=True, max_length=255, null=True, verbose_name='вознаграждение')),
                ('time_to_complete', models.DurationField(validators=[django.core.validators.MaxValueValidator(datetime.timedelta(seconds=120))], verbose_name='время на выполнение привычки')),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.habit', verbose_name='связанная привычка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habit', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mainapp.place', verbose_name='место')),
            ],
            options={
                'verbose_name': 'привычка',
                'verbose_name_plural': 'привычки',
            },
        ),
    ]