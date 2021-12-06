from django.contrib import admin

# Register your models here.
from .models import (
    ActivityType,
    Activity
)

admin.site.register((ActivityType, Activity))
