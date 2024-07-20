from django.urls import path
from rest_framework.routers import DefaultRouter

from mainapp.apps import MainappConfig
from mainapp.views import PlaceViewSet, HabitCreateAPIView, HabitListAPIView, HabitPersonalListAPIView, \
    HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView

app_name = MainappConfig.name

router = DefaultRouter()
router.register(r'place', PlaceViewSet, basename='place')

urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit/', HabitListAPIView.as_view(), name='habit_list'),
    path('habit/personal/', HabitPersonalListAPIView.as_view(), name='habit_personal_list'),
    path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_get'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_delete'),

] + router.urls
