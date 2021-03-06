from django.shortcuts import render

# Create your views here.
from product.models import Product, Category, Comment, Cart


def landing(request):
    categories = Category.objects.all()
    recent_posts = Product.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html',
                  {'recent_posts': recent_posts, 'categories': categories})


def mypage(request):
    recent_carts = Cart.objects.order_by('-pk')
    categories = Category.objects.all()
    recent_comments = Comment.objects.order_by('-pk')
    return render(request, 'single_pages/mypage.html',
                  {'recent_comments':recent_comments,
                   'categories': categories,
                   'recent_carts':recent_carts})

def about(request):
    categories = Category.objects.all()
    return render(request, 'single_pages/about.html',
                  {'categories': categories})

