import contextlib
import segno
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from segno import helpers
from rest_framework.permissions import IsAuthenticated


from .paginations import LargeResultsSetPagination
from .utils import (
    qr_code_for_urls,
    qr_code_for_vcard,
    user_information_by_qr_code,
    color_validation, get_country_info,
    get_city_info, get_device_info
)
from .models import (EmailQrCode, SmsQrCode, TextQrCode, TwitterQrCode, IpAddress, Country, City, Device,
                     UrlQrCode, VcardQrCode, WifiQrCode, Dashboard)
from .serializers import (EmailSerializer, SmsSerializer, TextSerializer, UrlDetailSerializer,
                          TwitterSerializer, UrlSerializer, VCardSerializer,
                          WifiSerializer, DashboardSerializer)


localhost = 'http://127.0.0.1:8000/media/'


class DashboardView(generics.GenericAPIView):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    # permission_classes = [IsAuthenticated]
    # pagination_class = LargeResultsSetPagination

    def get(self, request):
        url_qrs = Dashboard.objects.filter(user=self.request.user).order_by('-id')
        serializer = DashboardSerializer(url_qrs, many=True)
        return Response(serializer.data)


###################### Url Qr Code ###############################


class SingleUlrQrCode(generics.GenericAPIView):
    queryset = UrlQrCode.objects.all()
    serializer_class = UrlSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        data = user_information_by_qr_code(request)
        user_ip = data['my_ip']
        country = data['country']
        city = data['region']
        device = data['device_type']


        print("all ===================>>>>>>>>>",city, country, device)

        with contextlib.suppress(Exception):
            qr_id = request.GET.get('id')
            related_name = request.GET.get('related_name')
        print(qr_id, related_name)



        url_qr_code = UrlQrCode.objects.get(id=qr_id)
        country = Country.objects.get_or_create(name=country)
        city = City.objects.get_or_create(name=city)
        device = Device.objects.get_or_create(name=device)

        country_id = Country.objects.get(id=country[0].id)
        city_id = City.objects.get(id=country[0].id)
        device_id = Device.objects.get(id=country[0].id)

        ip_add = IpAddress.objects.create(ip=user_ip, city=city_id, country=country_id, device=device_id)
        url_qr_code.location.add(ip_add)

        url_qr_code.scan_count += 1
        url_qr_code.save()

        country_info = get_country_info(related_name, url_qr_code, request)
        city_info = get_city_info(related_name, url_qr_code)
        device_info = get_device_info(related_name, url_qr_code)

        all_data = [{'q_id': url_qr_code.id, 'country_info': country_info, 'city_info': city_info,
                    'device_info': device_info, 'logo_type': url_qr_code.logo_type, 'background': url_qr_code.background,
                    'symbol_color': url_qr_code.symbol_color, 'link': url_qr_code.link, 'color': url_qr_code.color
                    }]

        return Response(all_data, status=status.HTTP_200_OK)


class UrlQrCodeListCreateView(generics.GenericAPIView):
    queryset = UrlQrCode.objects.all()
    serializer_class = UrlSerializer
    # permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        instance = UrlQrCode.objects.all()
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(
                page, many=True,  context={"request": request}).data)
        else:
            serializer = self.serializer_class(
                instance, many=True,  context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        url = data['link']
        color = data['color']
        symbol_color = data['symbol_color']
        background = data['background']
        logo_type = data['logo_type']
        is_active = data['is_active']
        type_path = 'url_qr_codes/url'
        related_name = 'ip_address'

        if url == "":
            return Response('The field can not be empty')

        try:
            unique_id = int(UrlQrCode.objects.first().url_id) + 1
        except Exception:
            unique_id = 1


        if logo_type == 1:
            logo = 'static/logos/l1.png'
        elif logo_type == 2:
            logo = 'static/logos/l2.png'
        else:
            logo = 'static/logos/l0.png'

        if color == '':
            color = 'black'
        if symbol_color == '':
            symbol_color = 'black'
        if background == '':
            background = 'white'

        cl_validation = color_validation(color)
        if not cl_validation:
            return Response("This color is not available")

        symbol_color_validation = color_validation(symbol_color)
        if not symbol_color_validation:
            return Response("This symbol color is not available")

        background_validation = color_validation(background)
        if not background_validation:
            return Response("This background color is not available")

        qr_id = UrlQrCode.objects.create(color=color, link=url, logo_type=logo_type, user=self.request.user, background=background,
                        is_active=is_active, symbol_color=symbol_color, qr_image=f'{type_path}{unique_id}.png', url_id=unique_id)

        print(qr_id)

        try:
            dash = Dashboard.objects.get(user=request.user)
        except Exception:
            dash = Dashboard.objects.create(user=request.user)

        dash.url_qr.add(qr_id)
        dash.save()

        my_url = f'http://10.10.0.156:3000/redirect/?id={qr_id.id}/related_name={related_name}/params={url}/is_acitve={is_active}'
        qr_code_for_urls(color=color.lower(), symbol_color=symbol_color, background=background, logo=logo,
                         type_id=str(unique_id), qr_type=my_url, type_path=type_path)

        data = [{
                'qr_id': qr_id.id, 'user': self.request.user.username,
                'qr_code_url': qr_id.qr_image.url, 'is_active': qr_id.is_active,
                'color': color or 'black', 'symbol_color': symbol_color or 'black',
                'logo_type': logo_type or 0, 'background': background or 'white',
                }]

        return Response({'results': data}, status=status.HTTP_201_CREATED)


class UrlQrCodeDetailView(generics.GenericAPIView):
    queryset = UrlQrCode.objects.all()
    serializer_class = UrlDetailSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return UrlQrCode.objects.get(pk=pk)
        except UrlQrCode.DoesNotExist as e:
            raise Http404 from e

    def get(self, request, pk):
        url_qrcode = self.get_object(pk)
        serializer = UrlDetailSerializer(url_qrcode)
        return Response(serializer.data)

    def put(self, request, pk):
        url_qrcode = self.get_object(pk)
        serializer = UrlDetailSerializer(url_qrcode, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        url_qrcode = self.get_object(pk)
        serializer = UrlDetailSerializer(url_qrcode, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        url_qrcode = self.get_object(pk)
        url_qrcode.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


###################### Vcard Qr Code ############################

class VCardQrGeneratorListCreateView(generics.GenericAPIView):
    queryset = VcardQrCode.objects.all()
    serializer_class = VCardSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        instance = VcardQrCode.objects.all()
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(
                page, many=True,  context={"request": request}).data)
        else:
            serializer = self.serializer_class(
                instance, many=True,  context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        full_name = data['full_name']
        cellphone = data['cellphone']
        homephone = data['homephone']
        fax = data['fax']
        email = data['email']
        company = data['company']
        org = data['job']
        street = data['street']
        city = data['city']
        zipcode = data['zipcode']
        region = data['region']
        country = data['country']
        url = data['website']
        color = data['color']
        symbol_color = data['symbol_color']
        background = data['background']
        logo_type = data['logo_type']
        related_name = 'vcard_ip'
        type_path = 'vcard_qr_code/vcard'


        if full_name == "":
            return Response('The field First Name can not be empty')
        if cellphone == "":
            return Response('The field Cellphone can not be empty')

        try:
            unique_id = int(VcardQrCode.objects.last().url_id) + 1
        except Exception:
            unique_id = 1


        if logo_type == 1:
            logo = 'static/logos/l1.png'
        elif logo_type == 2:
            logo = 'static/logos/l2.png'
        else:
            logo = 'static/logos/l5.png'

        if color == '':
            color = 'black'
        if symbol_color == '':
            symbol_color = 'black'
        if background == '':
            background = 'white'

        cl_validation = color_validation(color)
        if not cl_validation:
            return Response("This color is not available")

        symbol_color_validation = color_validation(symbol_color)
        if not symbol_color_validation:
            return Response("This symbol color is not available")

        background_validation = color_validation(background)
        if not background_validation:
            return Response("This background color is not available")


        vcard = VcardQrCode.objects.create(
            full_name=full_name, cellphone=cellphone, homephone=homephone, user=self.request.user,
            email=email, fax=fax, company=company, job=org, street=street, url=url, symbol_color=symbol_color,
            city=city, zipcode=zipcode, region=region, country=country, color=color, url_id=unique_id,
            vcard_qr_image=f'{type_path}{unique_id}.png', background=background)

        try:
            dash = Dashboard.objects.get(user=request.user)
        except Exception:
            dash = Dashboard.objects.create(user=request.user)

        dash.vcard_qr.add(vcard)
        dash.save()

        vcard_last = qr_code_for_vcard(name=full_name, displayname=full_name, email=email, cellphone=cellphone, homephone=homephone,
                          fax=fax, company=company, street=street, city=city, zipcode=zipcode, url=url, type_path=type_path,
                          region=region, country=country,  color=color.lower(), org=org,  logo=logo, type_id=str(unique_id),
                          symbol_color=symbol_color, background=background
                        )
        qr_image_url =  "/media" + vcard_last.split("media")[1]

        my_url = f'http://10.10.0.156:3000/redirect/?id={vcard.id}/related_name={related_name}/params={qr_image_url}/'
        qr_code_for_urls(color=color.lower(), symbol_color=symbol_color, background=background, logo=logo,
                         type_id=str(unique_id)+'s', qr_type=my_url, type_path=type_path)


        data = [{'qr_code_url': qr_image_url,
                'full_name': full_name, 'cellphone': cellphone, 'homephone': homephone,
                 'fax': fax, 'company': company, 'job': org, 'street': street, 'country': country,
                 'city': city, 'zipcode': zipcode, 'region': region, 'url': url,  'email': email,
                 'color': color or 'black', 'logo_type': logo_type or 0}]

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class TexQrGeneratortListCreateView(generics.GenericAPIView):
    queryset = TextQrCode.objects.all()
    serializer_class = TextSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        instance = TextQrCode.objects.all()
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(
                page, many=True,  context={"request": request}).data)
        else:
            serializer = self.serializer_class(
                instance, many=True,  context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        text = data['text']
        logo_type = data['logo_type']
        color = data['color']
        type_path = 'text_qr_code/text'

        if text == "":
            return Response('The Text field can not be empty')

        if logo_type == 1:
            logo = 'static/logos/l1.png'
        elif logo_type == 2:
            logo = 'static/logos/l2.png'
        else:
            logo = 'static/logos/l3.png'

        text_qr = TextQrCode.objects.create(
            text=text, color=color, logo_type=logo_type)
        qr_code_for_urls(qr_type=text, color=color, logo=logo,
                         type_id=str(text_qr.id),  type_path=type_path)
        TextQrCode.save_qr_image(type_path, text_qr)

        data = [{
                'qr_code_url': f'http://127.0.0.1:8000/media/{type_path}{text_qr.id}.png',
                'text': text, 'color': color or None, 'logo_type': logo_type or None
                }]

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class EmailQrGeneratorView(generics.GenericAPIView):
    queryset = EmailQrCode.objects.all()
    serializer_class = EmailSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        subject = data['subject']
        message = data['message']
        is_tracking = data['is_tracking']

        if email == "":
            return Response('The Email field can not be empty')
        if subject == "":
            return Response('The Subject field can not be empty')

        qr = helpers.make_email(
            to=email,
            subject=subject,
            body=message
        )

        if color := data['color']:
            qr.save(
                f'{settings.MEDIA_ROOT}/email_qr_code/email{subject[:5]}.png', scale=15, dark=color)
        else:
            qr.save(
                f'{settings.MEDIA_ROOT}/email_qr_code/email{subject[:5]}.png', scale=15)

        data = [{
                'qr_code_url': f'http://127.0.0.1:8000/media/email_qr_code/email{subject[:5]}.png',
                'is_tracking': is_tracking
                }]

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class SmsQrGeneratorView(generics.GenericAPIView):
    queryset = SmsQrCode.objects.all()
    serializer_class = SmsSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        mobile = request.data['mobile']
        message = request.data['message']
        # is_tracking = request.data['is_tracking']

        if mobile == "":
            return Response('The mobile field can not be empty')

        qr = segno.make_qr(f'smsto:{mobile}:{message}')
        if color := data['color']:
            qr.save(
                f'{settings.MEDIA_ROOT}/sms_qr_code/sms{mobile[:5]}.png', scale=15, dark=color)
        else:
            qr.save(
                f'{settings.MEDIA_ROOT}/sms_qr_code/sms{mobile[:5]}.png', scale=15)

        data = [{
                'qr_code_url': f'http://127.0.0.1:8000/media/sms_qr_code/sms{mobile[:5]}.png',
                # 'is_tracking': is_tracking
                }]

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class WifiQrGeneratorView(generics.GenericAPIView):
    queryset = WifiQrCode.objects.all()
    serializer_class = WifiSerializer

    def post(self, request, *args, **kwargs):
        network_name = request.data['network_name']
        password = request.data['password']
        encryription_type = request.data['encryription_type']
        is_tracking = request.data['is_tracking']
        is_hidden = request.data['is_hidden']

        qr = helpers.make_wifi(
            ssid=network_name,
            password=password,
            security=encryription_type,
            hidden=is_hidden
        )
        qr.save(
            f'{settings.MEDIA_ROOT}/wifi_qr_code/wifi{network_name[:5]}.png', scale=15)

        data = [{
                'qr_code_url': f'http://127.0.0.1:8000/media/wifi_qr_code/wifi{network_name[:5]}.png',
                'is_tracking': is_tracking
                }]

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class TwitterQrGeneratorView(generics.GenericAPIView):
    queryset = TwitterQrCode.objects.all()
    serializer_class = TwitterSerializer

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        tweet = request.data['tweet']
        twitter_type = request.data['twitter_type']
        color = request.data['color']
        is_tracking = request.data['is_tracking']

        if twitter_type == 'Profile':
            if username == "":
                return Response('The Username field can not be empty')
        elif twitter_type == 'Post':
            if tweet == "":
                return Response('The Tweet field can not be empty')

        if twitter_type == 'Profile':
            qr = segno.make(f'https://twitter.com/{username[:5]}/')
            qr.save(
                f'{settings.MEDIA_ROOT}/twitter_qr_code/twitter{username[:5]}.png', scale=15, dark=color)

        elif twitter_type == 'Post':
            qr = segno.make(f'https://twitter.com/intent/tweet?text={tweet}')
            qr.save(
                f'{settings.MEDIA_ROOT}/twitter_qr_code/twitter{tweet[:5]}.png', scale=15, dark=color)

        data = [{
                'qr_code_url': f'http://127.0.0.1:8000/media/twitter_qr_code/twitter{username[:5]}{tweet[:5]}.png',
                'is_tracking': is_tracking
                }]

        return Response({'data': data}, status=status.HTTP_201_CREATED)
