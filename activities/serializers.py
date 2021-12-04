# drf imports
from rest_framework.serializers import (
    ModelSerializer
)

# model imports
from .models import (
    ActivityType
)


class ActivityTypeSerializer(ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ('id', 'name')
