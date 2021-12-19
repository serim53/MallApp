from django.urls import path
from . import views
# from .views import *

# app_name = 'product'

urlpatterns = [ # 서버IP/product/

    path('', views.landing),    # 대문페이지
    path('mypage/', views.mypage),   # 서버IP/mypage/
    path('about/', views.about),   # 서버IP/about
]