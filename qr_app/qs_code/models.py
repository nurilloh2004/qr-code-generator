from django.db import models
from django.db.models import Count
from django.db.models import F


from users.models import CustomUser




ENCRYPTION_TYPE = (
    ('None', 'None'),
    ('WPA/WPA2', 'WPA/WPA2'),
    ('WEP', 'WEP')
)


CRYPTOCURRENCY_TYPE = (
    ('Bitcoin', 'Bitcoin'),
    ('Bitcoin Cash', 'Bitcoin Cash'),
    ('Ether', 'Ether'),
    ('Litecoin', 'Litecoin'),
    ('Dash', 'Dash')
)

TWITTER_TYPE = (
    ('Profile', 'Profile'),
    ('Post', 'Post')
)


class CommonModelFields(models.Model):
    color = models.CharField(max_length=250, blank=True, null=True)
    logo_type = models.IntegerField(default=0)
    scan_count = models.IntegerField(default=0)
    background = models.CharField(max_length=250, blank=True, null=True)
    symbol_color = models.CharField(max_length=250, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-id', )


class Country(TimeStampModel):
    name = models.CharField(max_length=250, default='Uzbekistan')
    scan_count = models.IntegerField(default=0)


    class Meta:
        verbose_name_plural = 'Countries'
    

    def __str__(self):
        return f'{self.id} - {self.name}'


class City(TimeStampModel):
    name = models.CharField(max_length=250, default='Tashkent')
    scan_count = models.IntegerField(default=0)


    class Meta:
        verbose_name_plural = 'Cities'


    def __str__(self):
        return f'{self.id} - {self.name}'


class Device(TimeStampModel):
    name = models.CharField(max_length=250, default='PC')
    scan_count = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.id} - {self.name}'


class IpAddress(TimeStampModel):
    ip = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, default='84.54.74.20')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE) 


    class Meta:
        verbose_name_plural = 'IpAddresses'

    def __str__(self):
        return f'{self.city} - {self.country} - {self.device}'


class UrlQrCode(CommonModelFields, TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    link = models.URLField(max_length=10000)
    qr_image = models.ImageField(upload_to='url_qr_codes/', max_length=100, blank=True)
    location = models.ManyToManyField(IpAddress, related_name='ip_address')
    url_id = models.IntegerField(default=1)
    

    class Meta:
        verbose_name_plural = "UrlQrCodes"
        ordering = ['-id']
        
    def __str__(self):
        return str(self.id)         

    @property
    def get_device_info(self):
        device_data = []
        devices = Device.objects.all()
        for i in devices:
            device_count = IpAddress.objects.filter(device__name=i.name, ip_address__id=self.id)
            device = {
                'device_type': i.name,
                'count': device_count.count(),
            }
            device_data.append(device)
        return device_data

    @property
    def get_city_info(self):
        city_data = []
        cities = City.objects.all()
        for i in cities:
            city_count = IpAddress.objects.filter(city__name=i.name, ip_address__id=self.id)
            city = {
                'city_name': i.name,
                'count': city_count.count(),
            }
            city_data.append(city)
        return city_data

    @property
    def get_country_info(self):    
        country_data = []
        countries = Country.objects.all()
        for i in countries:
            country_count = IpAddress.objects.filter(country__name=i.name, ip_address__id=self.id)
            country = {
                'country_name': i.name,
                'count': country_count.count()
            }
            country_data.append(country)
        return country_data


class VcardQrCode(CommonModelFields, TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vcard_ip = models.ManyToManyField(IpAddress, related_name='vcard_ip')
    full_name = models.CharField(max_length=250)
    cellphone = models.CharField(max_length=250)
    homephone = models.CharField(max_length=250, blank=True, null=True)
    fax = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    company = models.CharField(max_length=250, blank=True, null=True)
    job = models.CharField(max_length=250, blank=True, null=True)
    street = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    zipcode = models.CharField(max_length=250, blank=True, null=True)
    region = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    vcard_qr_image = models.FileField(upload_to='vcard_qr_code/', max_length=100, blank=True)
    url_id = models.IntegerField(default=1)


    class Meta:
        verbose_name_plural = "VcardQrCodes"
        
    def __str__(self):
        return f'{self.id}'

    @property
    def get_device_info(self):
        device_data = []
        devices = Device.objects.all()
        for i in devices:
            device_count = IpAddress.objects.filter(device__name=i.name, ip_address__id=self.id)
            device = {
                'device_type': i.name,
                'count': device_count.count(),
            }
            device_data.append(device)
        return device_data

    @property
    def get_city_info(self):
        city_data = []
        cities = City.objects.all()
        for i in cities:
            city_count = IpAddress.objects.filter(city__name=i.name, ip_address__id=self.id)
            city = {
                'city_name': i.name,
                'count': city_count.count(),
            }
            city_data.append(city)
        return city_data

    @property
    def get_country_info(self):    
        country_data = []
        countries = Country.objects.all()
        for i in countries:
            country_count = IpAddress.objects.filter(country__name=i.name, ip_address__id=self.id)
            country = {
                'country_name': i.name,
                'count': country_count.count()
            }
            country_data.append(country)
        return country_data
    

class TextQrCode(CommonModelFields, TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text_ip = models.ManyToManyField(IpAddress, related_name='text_ip')
    text = models.TextField()
    text_qr_image = models.FileField(upload_to='text_qr_code/', max_length=100, blank=True) 
    url_id = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = "TextQrCodes"
        
    def __str__(self):
        return str(self.id)
    
    @property
    def get_device_info(self):
        device_data = []
        devices = Device.objects.all()
        for i in devices:
            device_count = IpAddress.objects.filter(device__name=i.name, ip_address__id=self.id)
            device = {
                'device_type': i.name,
                'count': device_count.count(),
            }
            device_data.append(device)
        return device_data

    @property
    def get_city_info(self):
        city_data = []
        cities = City.objects.all()
        for i in cities:
            city_count = IpAddress.objects.filter(city__name=i.name, ip_address__id=self.id)
            city = {
                'city_name': i.name,
                'count': city_count.count(),
            }
            city_data.append(city)
        return city_data

    @property
    def get_country_info(self):    
        country_data = []
        countries = Country.objects.all()
        for i in countries:
            country_count = IpAddress.objects.filter(country__name=i.name, ip_address__id=self.id)
            country = {
                'country_name': i.name,
                'count': country_count.count()
            }
            country_data.append(country)
        return country_data
    

class EmailQrCode(CommonModelFields, TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email_ip = models.ManyToManyField(IpAddress, related_name='email_ip')
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=250)
    message = models.TextField(blank=True, null=True)
    email_image = models.FileField(upload_to='email_qr_code/', max_length=100, blank=True)


    class Meta:
        verbose_name_plural = "EmailQrCodes"
        
    def __str__(self):
        return self.email
    
    @property
    def get_device_info(self):
        device_data = []
        devices = Device.objects.all()
        for i in devices:
            device_count = IpAddress.objects.filter(device__name=i.name, ip_address__id=self.id)
            device = {
                'device_type': i.name,
                'count': device_count.count(),
            }
            device_data.append(device)
        return device_data

    @property
    def get_city_info(self):
        city_data = []
        cities = City.objects.all()
        for i in cities:
            city_count = IpAddress.objects.filter(city__name=i.name, ip_address__id=self.id)
            city = {
                'city_name': i.name,
                'count': city_count.count(),
            }
            city_data.append(city)
        return city_data

    @property
    def get_country_info(self):    
        country_data = []
        countries = Country.objects.all()
        for i in countries:
            country_count = IpAddress.objects.filter(country__name=i.name, ip_address__id=self.id)
            country = {
                'country_name': i.name,
                'count': country_count.count()
            }
            country_data.append(country)
        return country_data


class SmsQrCode(CommonModelFields, TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sms_ip = models.ManyToManyField(IpAddress, related_name='sms_ip')
    phone = models.CharField(max_length=250)
    message = models.TextField(blank=True, null=True)
    url_id = models.IntegerField(default=1)
    sms_image = models.FileField(upload_to='sms_qr_code/', max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "SmsQrCodes"
        
    def __str__(self):
        return self.number

    @property
    def get_device_info(self):
        device_data = []
        devices = Device.objects.all()
        for i in devices:
            device_count = IpAddress.objects.filter(device__name=i.name, ip_address__id=self.id)
            device = {
                'device_type': i.name,
                'count': device_count.count(),
            }
            device_data.append(device)
        return device_data

    @property
    def get_city_info(self):
        city_data = []
        cities = City.objects.all()
        for i in cities:
            city_count = IpAddress.objects.filter(city__name=i.name, ip_address__id=self.id)
            city = {
                'city_name': i.name,
                'count': city_count.count(),
            }
            city_data.append(city)
        return city_data

    @property
    def get_country_info(self):    
        country_data = []
        countries = Country.objects.all()
        for i in countries:
            country_count = IpAddress.objects.filter(country__name=i.name, ip_address__id=self.id)
            country = {
                'country_name': i.name,
                'count': country_count.count()
            }
            country_data.append(country)
        return country_data


class WifiQrCode(CommonModelFields, TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wifi_ip = models.ManyToManyField(IpAddress, related_name='wifi_ip')
    network_name = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    encryription_type = models.CharField(choices=ENCRYPTION_TYPE, default='WPA/WPA2', max_length=10)
    is_hidden = models.BooleanField(default=False)
    url_id = models.IntegerField(default=1)
    wifi_image = models.FileField(upload_to='wifi_qr_code/', max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "WifiQrCodes"
        
    def __str__(self):
        return self.network_name

    @property
    def get_device_info(self):
        device_data = []
        devices = Device.objects.all()
        for i in devices:
            device_count = IpAddress.objects.filter(device__name=i.name, ip_address__id=self.id)
            device = {
                'device_type': i.name,
                'count': device_count.count(),
            }
            device_data.append(device)
        return device_data

    @property
    def get_city_info(self):
        city_data = []
        cities = City.objects.all()
        for i in cities:
            city_count = IpAddress.objects.filter(city__name=i.name, ip_address__id=self.id)
            city = {
                'city_name': i.name,
                'count': city_count.count(),
            }
            city_data.append(city)
        return city_data

    @property
    def get_country_info(self):    
        country_data = []
        countries = Country.objects.all()
        for i in countries:
            country_count = IpAddress.objects.filter(country__name=i.name, ip_address__id=self.id)
            country = {
                'country_name': i.name,
                'count': country_count.count()
            }
            country_data.append(country)
        return country_data


class TwitterQrCode(CommonModelFields, TimeStampModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    twitter_ip = models.ManyToManyField(IpAddress, related_name='twitter_ip')
    username = models.CharField(max_length=250, blank=True, null=True)
    tweet = models.TextField(blank=True, null=True)
    twitter_type = models.CharField(choices=TWITTER_TYPE, default='Profile', max_length=10)
    url_id = models.IntegerField(default=1)
    twitter_image = models.FileField(upload_to='twitter_qr_code/', max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "TwitterQrCode"
        
    def __str__(self):
        return self.username
    
    @property
    def get_device_info(self):
        device_data = []
        devices = Device.objects.all()
        for i in devices:
            device_count = IpAddress.objects.filter(device__name=i.name, ip_address__id=self.id)
            device = {
                'device_type': i.name,
                'count': device_count.count(),
            }
            device_data.append(device)
        return device_data

    @property
    def get_city_info(self):
        city_data = []
        cities = City.objects.all()
        for i in cities:
            city_count = IpAddress.objects.filter(city__name=i.name, ip_address__id=self.id)
            city = {
                'city_name': i.name,
                'count': city_count.count(),
            }
            city_data.append(city)
        return city_data

    @property
    def get_country_info(self):    
        country_data = []
        countries = Country.objects.all()
        for i in countries:
            country_count = IpAddress.objects.filter(country__name=i.name, ip_address__id=self.id)
            country = {
                'country_name': i.name,
                'count': country_count.count()
            }
            country_data.append(country)
        return country_data


class Dashboard(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    url_qr = models.ManyToManyField(UrlQrCode, related_name='url_dashboard')
    vcard_qr = models.ManyToManyField(VcardQrCode)
    text_qr = models.ManyToManyField(TextQrCode)
    email_qr = models.ManyToManyField(EmailQrCode)
    sms_qr = models.ManyToManyField(SmsQrCode)
    wifi_qr = models.ManyToManyField(WifiQrCode)
    twitter_qr = models.ManyToManyField(TwitterQrCode)


    class Meta:
        ordering = ['id']