from django.urls import path
from . import views
# from .views import *

# app_name = 'product'

urlpatterns = [ # 서버IP/product/

    path('', views.ProductList.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),

    path('search/<str:q>/', views.ProductSearch.as_view()),
    path('update_product/<int:pk>/', views.ProductUpdate.as_view()),
    path('create_product/', views.ProductCreate.as_view()),
    path('category/<str:slug>', views.category_page), # 서버 ip/blog/category/slug
    path('manufacturer/<str:slug>', views.manufacturer_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('<int:pk>/new_cart/', views.new_cart),
]