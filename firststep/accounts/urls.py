from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserSettingsViewSet, ActivityLogViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'settings', UserSettingsViewSet, basename='settings')
router.register(r'activities', ActivityLogViewSet, basename='activities')

urlpatterns = [
    path('', include(router.urls)),
]
