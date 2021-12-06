from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
from .models import *

# def index(request) :
#     products = Product.objects.all()
#     return render(request, 'product/index.html')

def product_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    return render(request, 'product/index.html',
                  {
                      'current_category':current_category,
                      'categories':categories,
                      'products':products
                  })

def product_detail(request, pk, product_slug=None):
    product = get_object_or_404(Product, pk=pk, slug=product_slug)
    return render(request, 'product/detail.html', {'product':product})
