# drf imports
from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    Serializer,
    IntegerField,
    CharField,
    ValidationError,
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

    def validate(self, data):
        if ActivityType.objects.filter(user=self.context['request'].user, name=data.get('name')).exists():
            raise ValidationError("'{}' for this user already exists!".format(data.get('name')))
        return data


class ActivitySerializer(ModelSerializer):
    activity_type = StringRelatedField()

    class Meta:
        model = Activity
        fields = ('id', 'time_spent', 'activity_type')


class FetchActivitiesSerializer(Serializer):
    id = IntegerField()
    name = CharField()  # activity_type name
    total_time_spent = CharField()
