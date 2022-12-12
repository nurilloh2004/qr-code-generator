import io, json, requests, segno
from segno import helpers
from django.conf import settings
from PIL import Image
from rest_framework.response import Response


from .models import (EmailQrCode, SmsQrCode, TextQrCode, TwitterQrCode, Country, Device, City, IpAddress,
                                                                                        UrlQrCode, VcardQrCode, WifiQrCode)



api_key = '948e85cbc23d471e85942b9a90174fed'

api_url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={api_key}&fields=ip_address,country,region'



def color_validation(color):
    cl_lst = ['red', 'orange', 'yellow', 'green', 'blue', 'grey', 'indigo', 'violet', 'purple', 'mint', 'amber', 'pink',
            'turquoise', 'off white', 'Beige', 'Azure', 'Cyan', 'Clay', 'Ruby', 'Rust', 'Peach', 'Mauve', 'Lavender', 'Burgundy',
            'Coral', 'Navy Blue', 'Mustard', 'Teal', 'Tan', 'Gold', 'Cream', 'Bronze', 'Magenta', 'Charcoal', 'Maroon', 'Olive',
            'Brown', 'Silver', 'black', 'white'
        ]

    if color.lower() in cl_lst:
        return color
    else:
        False


def qr_code_for_urls(qr_type, type_path, type_id, logo, color='black', symbol_color='black', background='white'):
    out = io.BytesIO()
    segno.make(qr_type, error='h').save(out, scale=12, dark=symbol_color, data_dark=color, light=background,  kind='png')
    out.seek(0)
    img = Image.open(out)
    img = img.convert('RGB')
    img_width, img_height = img.size
    logo_max_size = img_height // 3
    logo_img = Image.open(logo)
    logo_img.thumbnail((logo_max_size, logo_max_size), Image.LANCZOS)
    box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
    img.paste(logo_img, box)

    qr_path = f'{settings.MEDIA_ROOT}/{type_path}{type_id}.png'

    img.save(qr_path)


def qr_code_for_vcard(
        name, displayname, email, homephone, fax, country, org,
        city, region, zipcode, cellphone, company, url, street,
        type_path, type_id, logo, color='black', symbol_color='black',
        background='white'
    ):
    out = io.BytesIO()
    helpers.make_vcard(
        name=name, displayname=displayname, cellphone=cellphone,
        homephone=homephone, fax=fax, email=email, source=company,
        org=org, street=street, city=city, url=url,
        zipcode=zipcode, region=region, country=country
        ).save(out, scale=12, dark=symbol_color, data_dark=color, light=background, kind='png')
    out.seek(0)
    img = Image.open(out)
    img = img.convert('RGB')
    img_width, img_height = img.size
    logo_max_size = img_height // 6
    logo_img = Image.open(logo)
    logo_img.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)
    box = ((img_width - logo_img.size[0]) // 2, (img_height - logo_img.size[1]) // 2)
    img.paste(logo_img, box)

    qr_path = f'{settings.MEDIA_ROOT}/{type_path}{type_id}.png'

    img.save(qr_path)

    return qr_path


def get_ip_geolocation_data(ip_address):

    response = requests.get(api_url)

    return response.content


def user_information_by_qr_code(request):
    ip = ''
    ip_address = ''
    if x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'):
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    geolocation_json = get_ip_geolocation_data(ip)
    geolocation_data = json.loads(geolocation_json)
    country = geolocation_data['country']
    region = geolocation_data['region']


    device_type = ""
    if request.user_agent.is_mobile and request.user_agent.os.family:
        device_type = f"Mobile - {request.user_agent.os.family}"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    device_type = "PC" if request.user_agent.is_pc else 'Other'

    return {'my_ip': ip or ip_address, 'country': country, 'region': region, "device_type": device_type}


def get_country_info(related_name, qr_id_type, request):
    kwargs = {f'{related_name}__id': qr_id_type.id}
    coming_ip = user_information_by_qr_code(request)['my_ip']
    countries = Country.objects.all()
    for i in countries:
        c_count = IpAddress.objects.filter(country__name=i.name, **kwargs)
        i.save()
        country = {
            'country_name': i.name,
            "count": c_count.count(),
            'user_ip': coming_ip
        }
    return [country]


def get_city_info(related_name, qr_id_type):
    all_data = []
    kwargs = {f'{related_name}__id': qr_id_type.id}
    cities = City.objects.all()
    for i in cities:
        city_count = IpAddress.objects.filter(city__name=i.name, **kwargs)
        i.save()
        city = {
            'city_name': i.name
        }
        all_data.append(city)
    return all_data


def get_device_info(related_name, qr_id_type):
    all_data = []
    kwargs = {f'{related_name}__id': qr_id_type.id}
    devices = Device.objects.all()
    for i in devices:
        device_count = IpAddress.objects.filter(device__name=i.name, **kwargs)
        i.save()
        device = {
            'device_type': i.name
        }
        all_data.append(device)
    return all_data


