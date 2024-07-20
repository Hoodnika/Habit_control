from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from mainapp.models import Place, Habit
from mainapp.paginators import CustomPagination
from mainapp.permissions import IsOwner
from mainapp.serializer import PlaceSerializer, HabitSerializer


########_PLACE_#########
class PlaceViewSet(ModelViewSet):
    """
    API ednpoint для работы с моделью Place
    """
    serializer_class = PlaceSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        """
        В зависимости от запроса присваиваютяс определенные права доступа
        :return:
        """
        if self.action in ['create', 'list']:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Сохраняем созданный экземпляр Места с владельцем текущего пользователя
        """
        place = serializer.save(user=self.request.user)

    def get_queryset(self):
        return Place.objects.filter(user=self.request.user)


########_HABIT_#########
class HabitCreateAPIView(CreateAPIView):
    """
    API endpoint для создания Привычки(Habit)
    """
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)


class HabitListAPIView(ListAPIView):
    """
    API endpoint для получения всех публичных привычек
    """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = CustomPagination


class HabitPersonalListAPIView(ListAPIView):
    """
    API endpoint для получения всех привычек текущего пользователя
    """
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitRetrieveAPIView(RetrieveAPIView):
    """
    API endpoint для получения конкретной привычки текущего пользователя
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)


class HabitUpdateAPIView(UpdateAPIView):
    """
    API endpoint для изменения информации о привычке текущего пользователя
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsOwner,)

    def partial_update(self, request, *args, **kwargs):
        """
        Позволяет частично обновлять экземпляр через patch
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        habit = self.get_object()
        serializer = self.get_serializer(habit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class HabitDestroyAPIView(DestroyAPIView):
    """
    API endpoint для удаления привычки текущего пользователя
    """
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
