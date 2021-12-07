# drf imports
from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    Serializer,
    IntegerField,
    CharField,
    TimeField
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


class FetchActivitiesSerializer(Serializer):
    id = IntegerField()
    name = CharField()  # activity_type name
    total_time_spent = CharField()
