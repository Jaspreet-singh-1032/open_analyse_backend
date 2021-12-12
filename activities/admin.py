from django.contrib import admin

# Register your models here.
from .models import (
    ActivityType,
    Activity
)

admin.site.register((ActivityType))

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    fields = ('time_spent' , 'activity_type' , 'user' , 'created')
    readonly_fields = ('created' , )
