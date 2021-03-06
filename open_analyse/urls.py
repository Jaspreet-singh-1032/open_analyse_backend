"""open_analyse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# views import
# user
from user.views import (
    UserViewSet
)
# activities
from activities.views import (
    ActivityTypesViewSet,
    ActivitesViewSet
)
# social auth
from social_auth.views import (
    GoogleLoginView
)

router = routers.SimpleRouter()

# user
router.register(r'user', UserViewSet, basename='user')

# activities
router.register(r'activities/activity-types',
                ActivityTypesViewSet, basename='activity_types')
router.register(r'activities', ActivitesViewSet, basename='activities')

schema_view = get_schema_view(
    openapi.Info(
        title="openAnalyse",
        default_version='v1',
        description="Api's for openAnalyse",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('rest-auth/google/', GoogleLoginView.as_view(), name='google_login'),
]
