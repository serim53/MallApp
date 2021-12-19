from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms_cart import CartForm
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from .models import Product

# Create your views here.
from .models import *

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


def new_cart(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            comment_form = CartForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = post
                comment.author = request.user
                comment.save()
                return redirect("/mypage/")
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


# Create your views here.
class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'price']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(ProductCreate, self).form_valid(form)
            return response
        else:
            return redirect('/product/')


class ProductUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # 모델명_form
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'price']

    template_name = 'product/product_update_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def dispatch(self, request, *args, **kwargs):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class ProductList(ListView):
    model = Product
    ordering = '-pk'
    paginate_by = 8

    # template_name = 'product/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count()
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_post_count'] = Product.objects.filter(manufacturer=None).count()
        return context


class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count()
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_post_count'] = Product.objects.filter(manufacturer=None).count()
        context['comment_form'] = CommentForm
        return context


# post_detail.html
#
class ProductSearch(ProductList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        product_list = Product.objects.filter(
            Q(name__contains=q) | Q(manufacturer__name__contains=q) | Q(category__name__contains=q)
        ).distinct()
        return product_list

    def get_context_data(self, **kwargs):
        context = super(ProductSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q}({self.get_queryset().count()})'

        return context


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        product_list = Product.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        product_list = Product.objects.filter(category=category)

    return render(request, 'product/product_list.html', {

        'product_list': product_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Product.objects.filter(category=None).count(),
        'category': category
    })


def manufacturer_page(request, slug):
    categories = Category.objects.all()
    if slug == 'no_manufacturer':
        manufacturer = '미분류'
        product_list = Product.objects.filter(manufacturer=None)
    else:
        manufacturer = Manufacturer.objects.get(slug=slug)
        product_list = Product.objects.filter(manufacturer=manufacturer)

    return render(request, 'product/product_list.html', {

        'product_list': product_list,
        'manufacturers': Manufacturer.objects.all(),
        'no_manufacturer_post_count': Product.objects.filter(manufacturer=None).count(),
        'manufacturer': manufacturer,
        'categories': categories
    })