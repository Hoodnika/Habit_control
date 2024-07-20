from rest_framework.serializers import ModelSerializer

from mainapp.models import Habit, Place
from mainapp.validators import NoRewardWithRelated, NoRewardIfNice, NoRelatedIfNice, RelatedMustBeNice


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            NoRewardWithRelated(),
            NoRewardIfNice(),
            NoRelatedIfNice(),
            RelatedMustBeNice(),
        ]

