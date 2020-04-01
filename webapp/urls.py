from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import index, shopping_page, shopping_detail, add_to_cart, cart, acc_profile


urlpatterns = [
    path('', index, name='home'),
    path('accounts/profile/', acc_profile, name='profile'),
    path('shop/', shopping_page, name='shop'),

    path('shop/<id>/', shopping_detail, name='shop-detail'),
    path('add-cart/<id>/', add_to_cart, name='add-cart'),
    path('cart/', cart, name='cart')


]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

