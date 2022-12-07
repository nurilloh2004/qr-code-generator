from django.contrib import admin
from .models import UrlQrCode, SmsQrCode, TextQrCode, WifiQrCode, VcardQrCode, EmailQrCode, TwitterQrCode, IpAddress, City, \
    Country, Device, Dashboard


admin.site.register(UrlQrCode)
admin.site.register(SmsQrCode)
admin.site.register(TextQrCode)
admin.site.register(WifiQrCode)
admin.site.register(VcardQrCode)
admin.site.register(EmailQrCode)
admin.site.register(TwitterQrCode)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Device)
admin.site.register(IpAddress)
admin.site.register(Dashboard)