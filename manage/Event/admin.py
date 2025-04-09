# from django.contrib import admin
# from .models import Event, EventMetaData
#
#
# class EventMetaDataInLine(admin.StackedInline):
#     model = EventMetaData
#     can_delete = False
#     verbose_name_plural = 'EventMetaData'
#
#
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('name', 'owner', 'start_time', 'end_time', 'capacity', 'is_open')
#     search_fields = ('name', 'description', 'location', 'owner__username', 'owner__email')
#     list_filter = ('is_open', 'start_time', 'owner')
#     inlines = [EventMetaDataInLine]
#     filter_horizontal = ('participants',)
#     readonly_fields = ('owner',)
#
#     fieldsets = (
#         (None, {'fields': ('name', 'owner', 'description', 'location')}),
#         ('timing', {'fields': ('start_time', 'end_time')}),
#         ('capacity and status', {'fields': ('capacity', 'is_open')}),
#         (' principles', {'fields': ('participants',)}),
#     )
#
#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.owner = request.user
#             super().save_model(request, obj, form, change)
#
#
#
#
#
