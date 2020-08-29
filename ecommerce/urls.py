from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

from django.contrib.auth.views import LogoutView
from accounts.views import login_page, register_page, guest_register_view

from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from carts.views import cart_detail_api_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls', namespace='products')),
    path('search/', include("search.urls", namespace='search')),
    path('cart/', include("carts.urls", namespace='cart')),
    # auth start here
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/guest/', guest_register_view, name='guest_register'),
    # auth end here
    path('checkout/address/create/', checkout_address_create_view,
         name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view,
         name='checkout_address_reuse'),
    url('api/cart/', cart_detail_api_view, name='api-cart'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
