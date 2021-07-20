from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . views import  Shop,OrderSummaryView,CheckoutView
from django.conf.urls import url
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('base/', views.base, name='base'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<slug>/',views.add_to_cart, name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('signup/', views.registerPage, name='signup'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('contactus/', views.contactus, name='contactus'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('service/', views.service, name='service'),
    path('login/',views.user_login,name='login'),
    path('seeall/', views.see_all, name='seeall'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('<slug:slug>/shop/', Shop.as_view(), name='shop'),
    path('<slug:slug>/shopdetail/', views.shopdetail, name='shopdetail'),
    path('wishlist/', views.wishlist, name ='wishlist'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)