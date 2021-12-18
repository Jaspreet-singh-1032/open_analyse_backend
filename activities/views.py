# python imports
from datetime import datetime , timedelta

# django import
from django.db.models import Sum, Case, When, IntegerField

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
from django_filters.rest_framework import DjangoFilterBackend

# models import
from .models import (
    ActivityType,
    Activity
)

# serializers import
from .serializers import (
    ActivityTypeSerializer,
    ActivitySerializer,
    FetchActivitiesSerializer
)


class ActivityTypesViewSet(ListModelMixin, DestroyModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = ActivityTypeSerializer

    def get_queryset(self):
        return ActivityType.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], serializer_class=ActivitySerializer)
    def add_activity(self, request, pk):
        # add activity for a activity type
        activity_type = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, activity_type=activity_type)
            return Response(serializer.data , status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], serializer_class=FetchActivitiesSerializer,url_name='fetch_activities',)
    def fetch_activities(self, request):
        '''returns all activity_types and total time spend on each'''
        days = int(self.request.query_params.get('days') or 7)
        filter_days = datetime.now() - timedelta(days=days)

        queryset = self.filter_queryset(self.get_queryset())
        activities = queryset.values('id', 'name').annotate(
            total_time_spent=Sum(Case(
                When(activities__created__date__gte=filter_days.date() , then= 'activities__time_spent'),
                default=0,
                output_field=IntegerField()
            )))
        serializer = self.serializer_class(activities, many=True)
        return Response(serializer.data)
    

class ActivitesViewSet(ListModelMixin,GenericViewSet):
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'created':['lte','gte'],
    }

    def get_queryset(self):
        return Activity.objects.select_related('activity_type').filter(user = self.request.user).order_by('-created')
    
