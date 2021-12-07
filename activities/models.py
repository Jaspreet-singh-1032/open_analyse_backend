from django.db import models
from django_extensions.db.models import TimeStampedModel


class ActivityType(TimeStampedModel):
    # activity type (catagory) eg. reading_books , learn-django etc.
    name = models.CharField(max_length=100)

    # relations fields
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(TimeStampedModel):
    time_spent = models.TimeField()

    # relationship fields
    activity_type = models.ForeignKey(
        ActivityType, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
