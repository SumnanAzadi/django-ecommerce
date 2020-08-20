from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls', namespace='products')),
    path('search/', include("search.urls", namespace='search')),
    path('cart/', include("carts.urls", namespace='cart')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
