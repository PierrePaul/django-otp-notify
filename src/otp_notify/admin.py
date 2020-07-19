from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from .models import NotifySMSDevice


class NotifySMSDeviceAdmin(admin.ModelAdmin):
    """
    :class:`~django.contrib.admin.ModelAdmin` for
    :class:`~otp_notify.models.NotifySMSDevice`.
    """
    fieldsets = [
        ('Identity', {
            'fields': ['user', 'name', 'confirmed'],
        }),
        ('Configuration', {
            'fields': ['number'],
        }),
    ]
    raw_id_fields = ['user']


try:
    admin.site.register(NotifySMSDevice, NotifySMSDeviceAdmin)
except AlreadyRegistered:
    # Ignore the useless exception from multiple imports
    pass
