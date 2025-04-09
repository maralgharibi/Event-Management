from rest_framework import serializers
from django.contrib.auth import get_user_model
from Event.models import Event, EventMetaData
from User.serializers import UserSerializer

User = get_user_model()


class AdminUserSerializer(UserSerializer):
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    owned_events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    participated_events = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('is_staff', 'is_superuser', 'owned_events', 'participated_events', 'date_joined', 'is_active')
        read_only_fields = UserSerializer.Meta.read_only_fields + ('owned_events', 'participated_events', 'date_joined')


class AdminEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class AdminEventMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMetaData
        fields = '__all__'


class AdminSettingSerializer(serializers.Serializer):
    owned_events_limit = serializers.IntegerField()
