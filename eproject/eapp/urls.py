from django.contrib import admin
from django.urls import path 
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
  path('',views.home),  
  path('viewdetail/<pid>',views.viewdetail),
  path('catfilter/<cid>',views.catfilter),
  path('sort/<sid>',views.sort),
  path('register/',views.registration),
  path('login/',views.user_login),
  path('logout/',views.user_logout),
  path('addtocart/<pid>',views.addToCart),
  path('viewcart/',views.viewcart),
  path('remove/<cid>',views.removeFromCart),
  path('updateqty/<qv>/<cid>',views.updateqty),
  path('placeorder/',views.placeorder),
  path('pay',views.pay),
  path('range',views.range),
  path("senduseremail",views.sendusermail),
  path("dashboard/",views.dashboard),
  path("delete/<did>",views.delete)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

