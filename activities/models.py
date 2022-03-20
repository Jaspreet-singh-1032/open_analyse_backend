from django.db import models
from django_extensions.db.models import TimeStampedModel


class ActivityType(TimeStampedModel):
    # activity type (catagory) eg. reading_books , learn-django etc.
    name = models.CharField(max_length=100)

    # relations fields
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'], name='unique_activitytype')
        ]


class Activity(TimeStampedModel):
    time_spent = models.IntegerField()  # in seconds
    description = models.CharField(max_length=500, blank=True, null=True)

    # relationship fields
    activity_type = models.ForeignKey(
        ActivityType, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
