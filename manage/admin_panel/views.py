from django.shortcuts import render

from .serializers import AdminUserSerializer,AdminEventMetadataSerializer, AdminEventSerializer,AdminSettingSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from User.models import User
from Event.models import Event, EventMetaData

from django.db.models import Count
from django.utils import timezone


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'date_joined']

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        user = self.get_object()
        owned_events = Event.objects.filter(owner=user)
        participated_events = user.participants.all()
        return Response({
            'owned_events': [event.id for event in owned_events],
            'participated_events': [event.id for event in participated_events],
        })


class AdminEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-start_time')
    serializer_class = AdminEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    search_fields = ['name', 'description', 'location', 'owner__username']
    ordering_fields = ['name', 'start_time', 'end_time', 'capacity', 'is_open']

    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        event = self.get_object()
        participants = event.participants.all()
        serializer = AdminUserSerializer(participants, many=True, read_only=True)
        return Response(serializer.data)


class AdminEventMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EventMetaData.objects.all()
    serializer_class = AdminEventMetadataSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_fields = ['status', 'event']


class AdminSettingViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def list(self, request):
        default_owned_events_limit = User._meta.get_field('owned_events_limit').default
        return Response({'owned_events_limit': default_owned_events_limit})

    def update(self, request):
        serializer = AdminSettingSerializer(data=request.data)
        if serializer.is_valid():
            new_limit = serializer.validated_data['owned_events_limit']
            User.objects.all().update(owned_events_limit=new_limit)
            return Response({'owned_events_limit': new_limit})
        return Response(serializer.errors, status=400)


class AdminReportViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def list(self, request):
        total_users = User.objects.count()
        total_events = Event.objects.count()
        open_events = Event.objects.filter(is_open=True).count()
        closed_events = Event.objects.filter(is_open=False).count()
        popular_events = Event.objects.annotate(num_participants=Count('participants')).order_by('-num_participants')[:10]
        popular_events_data = [{'id': event.id, 'name': event.name, 'participants': event.num_participants} for event in popular_events]

        thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
        events_last_30_days = Event.objects.filter(EventMetadata__created_at__gte=thirty_days_ago).count()

        return Response({
            'total_users': total_users,
            'total_events': total_events,
            'open_events': open_events,
            'closed_events': closed_events,
            'popular_events': popular_events_data,
            'events_created_last_30_days': events_last_30_days
        })

