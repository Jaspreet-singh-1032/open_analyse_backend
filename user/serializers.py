# drf imports
from rest_framework.serializers import (
    Serializer,
    CharField,
    EmailField,
    IntegerField,
    ValidationError
)

# models import
from .models import User


class UserSerializer(Serializer):
    id = IntegerField(read_only=True)
    email = EmailField(max_length=50)
    username = CharField(max_length=30, required=False)
    password = CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        if User.objects.filter(email=validated_data.get('email')).exists():
            raise ValidationError({'email': ['email already exists']})
        user = User(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
