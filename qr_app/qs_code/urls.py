from django.urls import path 



from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('single-url-qrcode/', views.SingleUlrQrCode.as_view(), name='single_url_qrcodes'), #this url can be used with id in param
    path('url-list-create/', views.UrlQrCodeListCreateView.as_view(), name='url_list_create'),
    path('url-qr-detail/<int:pk>/', views.UrlQrCodeDetailView.as_view(), name='url_qr_code_detail'),

    path('vcard-list-create/', views.VCardQrGeneratorListCreateView.as_view(), name='vcard_list_create'),

    path('text-list-create/', views.TexQrGeneratortListCreateView.as_view(), name='text_list_create'),

    path('email/', views.EmailQrGeneratorView.as_view(), name='email_qrcode'),
    path('sms/', views.SmsQrGeneratorView.as_view(), name='sms_qrcode'),
    path('wifi/', views.WifiQrGeneratorView.as_view(), name='wifi_qrcode'),
    path('twitter/', views.TwitterQrGeneratorView.as_view(), name='twitter_qrcode'),

]
