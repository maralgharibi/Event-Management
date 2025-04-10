# Generated by Django 5.1.7 on 2025-03-31 09:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Event', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(related_name='participated_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventmetadata',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Event.event'),
        ),
    ]
