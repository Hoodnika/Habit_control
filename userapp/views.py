from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mainapp.paginators import CustomPagination
from userapp.models import User
from mainapp.permissions import IsMe, IsAdmin
from userapp.serializer import UserSerializer, UserCensoredSerializer


class UserCreateAPIView(CreateAPIView):
    """
    'API endpoint' для регистрации
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Получаем детальную информацию о конкретном пользователе
    Доступно только для текущего пользователя
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsMe,)


class UserUpdateAPIView(UpdateAPIView):
    """
    Изменяем информацию о конкретном пользователе
    Пользватель может изменять только свой профиль
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsMe,)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserDestroyAPIView(DestroyAPIView):
    """
    Удаляем конкретного пользователя
    Пользватель может удалять только свой профиль
    """
    queryset = User.objects.all()
    permission_classes = (IsMe,)


class UserListAPIView(ListAPIView):
    """
    Получаем список всех пользователей
    Доступно только для Admin
    """
    serializer_class = UserCensoredSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination
    permission_classes = (IsAdmin,)
