from django.contrib import admin
from django.contrib.auth import get_user_model
from Event.models import Event, EventMetaData
from .models import AdminSettings

User = get_user_model()


@admin.register(AdminSettings)
class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (' personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (' dates', {'fields': ('last_login', 'date_joined')}),
        ('limits', {'fields': ('owned_events_limit',)}),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'start_time', 'end_time', 'capacity', 'is_open')
    search_fields = ('name', 'description', 'location', 'owner__username')
    list_filter = ('is_open', 'start_time', 'end_time', 'owner')
    ordering = ('-start_time',)
    filter_horizontal = ('participants',)
    readonly_fields = ('owner',)
    fieldsets = (
        (None, {'fields': ('name', 'owner', 'description', 'location')}),
        ('timing', {'fields': ('start_time', 'end_time')}),
        ('capacity and status', {'fields': ('capacity', 'is_open')}),
        (' principles', {'fields': ('participants',)}),
    )


@admin.register(EventMetaData)
class EventMetadataAdmin(admin.ModelAdmin):
    list_display = ('event', 'created_at', 'updated_at', 'status')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    raw_id_fields = ('event',) # نمایش به صورت ID برای بهبود عملکرد در صورت وجود تعداد زیاد رویداد
