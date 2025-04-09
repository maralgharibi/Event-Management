from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Event, EventMetaData
from .serializers import EventSerializers, EventMetaDataSerializers, EventCreateSerializer, EventUpdateSerializer, \
    EventDetailSerializers
from .permissions import IsOwnerOrReadOnly
from User.models import User


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializers
        elif self.action == 'create':
            return EventCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return EventUpdateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        user = request.user
        open_events_count = user.owned_events.filter(is_open=True).count()
        if open_events_count >= user.owned_events_limit:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'error': 'You have reached the limit for open events.'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        detailed_serializer = EventDetailSerializers(serializer.instance)
        return Response(detailed_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        EventMetaData.objects.create(event=serializer.instance)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.participants.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Cannot delete event with participants.'})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def join(self, request, pk=None):
        event = self.get_object()
        user = request.user
        if not event.is_open:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'This event is closed.'})
        if event.participants.filter(id=user.id).exists():  # Use user.id for comparison
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'You are already participating in this event.'})
        if event.capacity > event.participants.count():
            event.participants.add(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'This event is full.'})

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        event = self.get_object()
        user = request.user
        if event.participants.filter(id=user.id).exists():
            event.participants.remove(user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'You are not participating in this event.'})

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly])
    def owner_details(self, request, pk=None):
        event = self.get_object()
        serializer = EventDetailSerializers(event)
        return Response(serializer.data)
