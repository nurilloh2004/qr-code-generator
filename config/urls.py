from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static



schema_view = get_schema_view(
   openapi.Info(
      title="Qr Code Generator API",
      default_version='v1',
   ),
   public=True,
)



urlpatterns = [
   path('admin/', admin.site.urls),
   path('users/', include('users.urls')),
   path('qr-code/', include('qs_code.urls')),

   path("r/", include("urlshortner.urls")),
   path('api-auth/', include('rest_framework.urls')),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]



if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)