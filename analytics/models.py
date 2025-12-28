from django.db import models
from django.utils.translation import gettext_lazy as _

# https://pypi.org/project/user-agents/
"""
from user_agents import parse

# iPhone's user agent string
ua_string = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
user_agent = parse(ua_string)

# Accessing user agent's browser attributes
user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
user_agent.browser.family  # returns 'Mobile Safari'
user_agent.browser.version  # returns (5, 1)
user_agent.browser.version_string   # returns '5.1'

# Accessing user agent's operating system properties
user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
user_agent.os.family  # returns 'iOS'
user_agent.os.version  # returns (5, 1)
user_agent.os.version_string  # returns '5.1'

# Accessing user agent's device properties
user_agent.device  # returns Device(family=u'iPhone', brand=u'Apple', model=u'iPhone')
user_agent.device.family  # returns 'iPhone'
user_agent.device.brand # returns 'Apple'
user_agent.device.model # returns 'iPhone'

# Viewing a pretty string version
str(user_agent) # returns "iPhone / iOS 5.1 / Mobile Safari 5.1"
Currently these attributes are supported:

    is_mobile: whether user agent is identified as a mobile phone (iPhone, Android phones, Blackberry, Windows Phone devices etc)
    is_tablet: whether user agent is identified as a tablet device (iPad, Kindle Fire, Nexus 7 etc)
    is_pc: whether user agent is identified to be running a traditional "desktop" OS (Windows, OS X, Linux)
    is_touch_capable: whether user agent has touch capabilities
    is_bot: whether user agent is a search engine crawler/spider

"""
class RequestLog(models.Model):
    class DeviceChoices(models.TextChoices):
        MOBILE = 'mobile', _("Mobile")
        TABLET = 'tablet', _("Tablet")
        DESKTOP = 'desktop', _("Desktop")
        BOT = 'bot', _("Bot")
        NA = '', _("Not applied")
        
    datetime = models.DateTimeField(auto_now_add=True)    
    ip_address = models.GenericIPAddressField()
    requested_url = models.URLField()
    requested_url_origin = models.TextField(blank=True)
    user_agent = models.TextField()
    operating_system = models.CharField(max_length=100, null=True, blank=True)
    device_type = models.CharField(max_length=10, choices=DeviceChoices.choices, default=DeviceChoices.NA)
    is_authenticated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.datetime} - {self.requested_url} - {self.ip_address}"
