import logging
from django.utils.deprecation import MiddlewareMixin
from user_agents import parse
from .models import RequestLog

logger = logging.getLogger(__name__)

class AnalyticsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            # Gather request data
            ip_address = self.get_client_ip(request)
            requested_url = request.build_absolute_uri()
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            is_authenticated = request.user.is_authenticated
            
            # Determine device type and OS
            user_agent_parsed = parse(user_agent)
            operating_system = user_agent_parsed.os.family if user_agent_parsed.os else None
            
            device_type = ''
            if user_agent_parsed.is_mobile:
                device_type = RequestLog.DeviceChoices.MOBILE    
            elif user_agent_parsed.is_tablet:
                device_type = RequestLog.DeviceChoices.TABLET
            elif user_agent_parsed.is_bot:
                device_type = RequestLog.DeviceChoices.BOT
            elif user_agent_parsed.is_pc:
                device_type = RequestLog.DeviceChoices.DESKTOP
            
            
            # Create a new log entry
            RequestLog.objects.create(
                ip_address=ip_address,
                requested_url=requested_url,
                user_agent=user_agent,
                operating_system=operating_system,
                device_type=device_type,
                is_authenticated=is_authenticated
            )
        except Exception as e:
            logger.error(f"Error logging request data: {e}")
            # Optionally handle the error or ignore it

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    