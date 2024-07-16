"""
URL configuration for foodProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from foodApp import views
from foodApp.views import homeMade

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register,name='register'),
    # path('chefregister',views.chefregister,name='chefregister'),
    path('login',views.login,name='login'),
    path('homeMade',homeMade.as_view(),name='home_made'),
    path('search/',views.search,name='search'),
    path('join',views.join,name='join'),
    path('delivery',views.delivery,name='delivery'),
    path('service',views.service,name='service'),
    path('foodItem',views.foodItem,name='foodItem'),
    # path('dailyMenu',views.dailyMenu,name='dailyMenu'),
    path('location',views.location,name='location'),
    path('chefloc/<int:pk>',views.chefloc,name='chefloc'),
    path('dailyMenu/<int:pk>',views.dailyMenu,name='dailyMenu'),
    path('addToCart',views.addToCart,name='addToCart'),
    path('viewcart',views.viewcart,name='viewcart'),
    path('changequantity',views.changequantity,name='changequantity'),
    path('summarypage',views.summary,name="summary"),
    path('showloc',views.showloc,name="showloc"),
    path('paymentsuccess',views.paymentsuccess,name='paymentsuccess'),
    path('logout',views.logout,name='logout'),
    path('newtamplate',views.newtemplate,name='newtemplate')




]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
