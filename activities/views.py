# drf imports
from rest_framework.viewsets import (
    GenericViewSet
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# models import
from .models import (
    ActivityType
)

# serializers import
from .serializers import (
    ActivityTypeSerializer
)


class ActivityTypesViewSet(ListModelMixin, DestroyModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = ActivityTypeSerializer

    def get_queryset(self):
        return ActivityType.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
