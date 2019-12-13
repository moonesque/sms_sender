from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'address', 'est_date', 'email']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=150,
        validators=[UnicodeUsernameValidator(), UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=128)
    password_repeat = serializers.CharField(max_length=128)
