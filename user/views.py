# django imports
from django.conf import settings
from django.contrib.auth import authenticate

# drf imports
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# serializers import
from .serializers import UserSerializer


class UserViewSet(ListModelMixin, GenericViewSet):
    serializer_class = UserSerializer

    def list(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data.get(
                'email'), password=serializer.validated_data.get('password'))
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'detail': 'login success', 'token': token.key})
            return Response({'detail': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'detail': 'registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
