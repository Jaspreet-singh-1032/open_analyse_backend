# drf imports
from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField
)

# model imports
from .models import (
    ActivityType,
    Activity
)


class ActivityTypeSerializer(ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ('id', 'name')


class ActivitySerializer(ModelSerializer):
    activity_type = StringRelatedField()

    class Meta:
        model = Activity
        fields = ('id', 'time_spent', 'activity_type')
