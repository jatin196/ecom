from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (index,
                    shopping_page,
                    shopping_detail,
                    add_to_cart,
                    cart,
                    remove_from_cart,
                    CheckoutView,
                    remove_single_from_cart,
                    PaymentView
                    )

urlpatterns = [
    path('', index, name='home'),
    # path('accounts/profile/', acc_profile, name='profile'),
    path('shop/', shopping_page, name='shop'),
    path('shop/<id>/', shopping_detail, name='shop-detail'),
    path('add-cart/<id>/', add_to_cart, name='add-cart'),
    path('remove-item/<id>/', remove_from_cart, name='remove-item'),
    path('remove-single-item/<id>/', remove_single_from_cart, name='remove-single-item'),
    path('checkout-detail/', CheckoutView.as_view(), name='checkout-detail'),
    path('cart/', cart, name='cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    # import debug_toolbar
    # urlpatterns += [path('__debug__/'), index, include(debug_toolbar.urls)]


