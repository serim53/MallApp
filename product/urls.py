from django.urls import path
from . import views
# from .views import *

# app_name = 'product'

urlpatterns = [ # 서버IP/product/
    # path('', product_in_category, name='product_all'),
    # path('<slug:category_slug>/', product_in_category, name='product_in_category'),
    # path('<int:id>/<product_slug>/', product_detail,
    #      name='product_detail'),

    # FBV
    # path('', views.product_in_category),
    # path('<int:pk>/', views.product_detail)

    # CBV
    path('', views.ProductList.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),
    #
    path('search/<str:q>/', views.ProductSearch.as_view()),
    path('update_product/<int:pk>/', views.ProductUpdate.as_view()),
    path('create_product/', views.ProductCreate.as_view()),
    # path('tag/<str:slug>', views.tag_page),
    path('category/<str:slug>', views.category_page), # 서버 ip/blog/category/slug
    path('<int:pk>/new_comment/', views.new_comment),
]