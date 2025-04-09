from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('users/me/', views.UserViewSet.as_view({'get': 'me'}), name='users'),
    path('users/login/', views.UserViewSet.as_view({'post': 'login'}), name='user-login'),
] + router.urls