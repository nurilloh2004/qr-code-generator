from rest_framework import serializers
from django.db.models import Q, Count, IntegerField, Case, When



from .models import (
    UrlQrCode, VcardQrCode, TextQrCode, EmailQrCode, SmsQrCode, WifiQrCode, TwitterQrCode, Device, IpAddress, City, Country,
    Dashboard, CommonModelFields
)
from users.models import CustomUser
from users.serializers import UserListSerializer



class UrlSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    scan_count = serializers.IntegerField(read_only=True)


    class Meta:
        model = UrlQrCode
        fields = ['id', 'user', 'link', 'color', 'logo_type', 'background', 'symbol_color', 'scan_count', 'photo_url',
                                                                                                     'is_active', 'created_at']

    def get_photo_url(self, obj):
        return obj.qr_image.url


class UrlDetailSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    user = UserListSerializer(read_only=True)
    country_info = serializers.ListField(source='urlqrcode.get_country_info')
    city_info = serializers.ListField(source='urlqrcode.get_city_info')
    device_info = serializers.ListField(source='urlqrcode.get_device_info')
    total_scans = serializers.IntegerField(source='urlqrcode.scan_count')


    class Meta:
        model = UrlQrCode
        fields = ['id', 'user', 'link', 'color', 'logo_type', 'background', 'symbol_color', 'photo_url',
                        'country_info', 'city_info', 'device_info',  'total_scans',
                        'is_active', 'created_at']

    def get_photo_url(self, obj):
        return obj.qr_image.url


class VCardSerializer(serializers.ModelSerializer):
    # photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    is_active = serializers.BooleanField(default=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = VcardQrCode
        fields = ['id', 'user', 'full_name', 'cellphone', 'homephone', 'fax', 'email', 'company', 'job', 'city',
        'zipcode', 'region', 'country', 'url', 'color', 'logo_type', 'street', 'created_at', 'is_active']


class TextSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    is_active = serializers.BooleanField(default=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = TextQrCode
        fields = ['id', 'user', 'text', 'color', 'logo_type', 'photo_url', 'created_at', 'is_active']

    def get_photo_url(self, obj):
        return obj.text_image.url


class EmailSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    is_active = serializers.BooleanField(default=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = EmailQrCode
        fields = ['id', 'user', 'email', 'subject', 'message', 'color', 'logo_type', 'photo_url', 'created_at', 'is_active']

    def get_photo_url(self, obj):
        return obj.url_qr.email_image.url


class SmsSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    is_active = serializers.BooleanField(default=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SmsQrCode
        fields = ['id', 'user', 'phone', 'message', 'color', 'photo_url', 'created_at', 'is_active']

    def get_photo_url(self, obj):
        return obj.sms_image.url


class WifiSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    is_active = serializers.BooleanField(default=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = WifiQrCode
        fields = ['id', 'user', 'network_name', 'password', 'encryription_type', 'color', 'logo_type', 'photo_url',
                                                                                 'created_at', 'is_active', 'is_hidden']

    def get_photo_url(self, obj):
        return obj.wifi_image.url


class TwitterSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M", read_only=True)
    is_active = serializers.BooleanField(default=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = TwitterQrCode
        fields = ['id', 'user', 'username', 'tweet', 'twitter_type', 'color', 'logo_type', 'photo_url', 'created_at', 'is_active']

    def get_photo_url(self, obj):
        return obj.twitter_image.url


class DashboardSerializer(serializers.ModelSerializer):
    url_qr = UrlDetailSerializer(read_only=True, many=True)
    all_url_qrcodes = serializers.SerializerMethodField(read_only=True)
    active_url_qrcodes = serializers.SerializerMethodField(read_only=True)
    inactive_url_qrcodes = serializers.SerializerMethodField(read_only=True)
    vcard_qr = VCardSerializer(read_only=True,  many=True)
    # text_qr = TextSerializer(read_only=True)
    # sms_qr = SmsSerializer(read_only=True)
    # email_qr = EmailSerializer(read_only=True)
    # wifi_qr = WifiSerializer(read_only=True)
    # twitter_qr = TwitterSerializer(read_only=True)


    class Meta:
        model = Dashboard
        fields = ('id', 'all_url_qrcodes', 'active_url_qrcodes', 'inactive_url_qrcodes', 'url_qr', 'vcard_qr', )

    def get_all_url_qrcodes(self, obj):
        return UrlQrCode.objects.all().count()

    def get_active_url_qrcodes(self, obj):
        return Dashboard.objects.filter(url_qr__is_active=True).count()


    def get_inactive_url_qrcodes(self, obj):
        return Dashboard.objects.filter(url_qr__is_active=False).count()





class UpdateSomeDatasSerializer(serializers.ModelSerializer):

    class Meta:
        model = UrlQrCode
        fields = ['link', 'color', 'background', 'symbol_color', 'logo_type']
