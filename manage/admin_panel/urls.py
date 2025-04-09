from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.AdminUserViewSet, basename='admin-user')
router.register(r'events', views.AdminEventViewSet, basename='admin-event')
router.register(r'event-metadata', views.AdminEventMetadataViewSet, basename='admin-event-metadata')
router.register(r'settings', views.AdminSettingViewSet, basename='admin-setting')
router.register(r'reports', views.AdminReportViewSet, basename='admin-report')

urlpatterns = [
    path('admin/api/', include(router.urls)),
]