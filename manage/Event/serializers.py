from rest_framework import serializers
from .models import Event, EventMetaData
from User.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class EventMetaDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = EventMetaData
        fields = ('created_at', 'updated_at', 'status', 'logs')
        read_only_fields = ('created_at', 'updated_at')


class EventSerializers(serializers.ModelSerializer):
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ('id', 'owner', 'name', 'description', 'capacity', 'start_time', 'end_time', 'location', 'is_open',
                  'participants_count')
        read_only_fields = ('id', 'owner', 'participants_count')

    def get_participants_count(self, obj):
        return obj.participants.count()


class EventDetailSerializers(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    metadata = EventMetaDataSerializers(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'owner', 'name', 'description', 'capacity', 'start_time', 'end_time', 'location', 'is_open', 'participants', 'metadata')
        read_only_fields = ('id', 'owner', 'participants', 'metadata')

    def create(self, validated_data):
        validated_data["owner"] =self.context['request'].user
        return Event.objects.create(**validated_data)


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'capacity', 'start_time', 'end_time', 'location')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return Event.objects.create(**validated_data)

    def validate_capacity(self, value):
        if value <= 0:
           raise serializers.ValidationError("Capacity must be greater than 0")
        return value

    def validate_start_time(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Start time cannot be in the past.")
        return value


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'capacity', 'start_time', 'end_time', 'location', 'is_open')
        read_only_fields = ['owner']
