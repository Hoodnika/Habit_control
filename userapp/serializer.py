from rest_framework.serializers import ModelSerializer

from userapp.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'tg_username', 'phone', 'avatar', 'country', 'password']


class UserCensoredSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'tg_username', 'phone', 'avatar', 'country']
