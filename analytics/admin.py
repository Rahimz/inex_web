from django.contrib import admin

from .models import RequestLog

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'datetime', 'device_type', 'operating_system',  'ip_address', 'requested_url']
    search_fields = ['ip_address', 'requested_url']
    
