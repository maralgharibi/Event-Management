from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Event(models.Model): #نگهداری اطلاعات اصلی و ذاتی یک رویدا
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='owned_events', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    start_time = models.DateField()
    end_time = models.DateField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participated_events')
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        unique_together = ('name', 'location', 'start_time')

    def can_be_deleted(self):
        return not self.participants.exists()

    def has_available_capacity(self):
        return self.participants.count() < self.capacity

    def is_user_participating(self, user):
        return self.participants.filter(id=user.id).exists()

    def add_participant(self, user):
        if self.is_open and self.has_available_capacity() and not self.is_user_participating(user):
            self.participants.add(user)
            return True
        return False

    def remove_participant(self, user):
        if self.is_user_participating(user):
            self.participants.remove(user)
            return True
        return False


class EventMetaData(models.Model): #نگهداری اطلاعات تکمیلی و فراداده
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="eventmetadata")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=[('open', 'Open'), ('closed', 'Closed')])
    logs = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Event Meta Data'
        verbose_name_plural = 'Event Meta Data'

