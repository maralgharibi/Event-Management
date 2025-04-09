from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    owned_events_limit = models.IntegerField(null=True, blank=True, default=10)

    def __str__(self):
        return self.username