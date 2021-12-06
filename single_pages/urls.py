from django.urls import path
from . import views
# from .views import *

# app_name = 'product'

urlpatterns = [ # 서버IP/product/
    # path('', product_in_category, name='product_all'),
    # path('<slug:category_slug>/', product_in_category, name='product_in_category'),
    # path('<int:id>/<product_slug>/', product_detail,
    #      name='product_detail'),

    path('', views.landing),    # 대문페이지
    path('about_me/', views.about_me)   # 서버IP/about_me
]