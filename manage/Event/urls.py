from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('events', views.EventViewSet, basename='events')
urlpatterns = [
    path('events/<int:pk>/join/', views.EventViewSet.as_view({'post':'join'}), name='event_join'),
    path('events/<int:pk>/leave/', views.EventViewSet.as_view({'post':'leave'}), name='event_leave'),
    path('events/<int:pk>/owner-details/', views.EventViewSet.as_view({'get':'owner-details'}), name='event_owner-details'),
] + router.urls