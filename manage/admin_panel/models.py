from django.db import models


class AdminSettings(models.Model):
    key = models.CharField(max_length=10, primary_key=True)
    value = models.TextField()

    def __str__(self):
        return self.key