from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from .models import Product

# Create your views here.
from .models import *


# def index(request) :
#     products = Product.objects.all()
#     return render(request, 'product/product_list.html')
#
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductUpdate,self).get_context_data()
    #     if self.object.tags.exists() :
    #         tags_str_list = list()
    #         for t in self.object.tags.all() :
    #             tags_str_list.append(t.name)
    #         context['tag_str_default'] = '; '.join(tags_str_list)
    #     return context

    # def form_valid(self, form):
    #     response = super(ProductUpdate, self).form_valid(form)
    #     self.object.tags.clear()
    #     tags_str = self.request.POST.get('tags_str')
    #     if tags_str:
    #         tags_str = tags_str.strip()
    #         tags_str = tags_str.replace(',', ';')
    #         tags_list = tags_str.split(';')
    #         for t in tags_list:
    #             t = t.strip()
    #             tag, is_tag_created = Tag.objects.get_or_create(name=t)
    #             if is_tag_created:
    #                 tag.slug = slugify(t, allow_unicode=True)
    #                 tag.save()
    #             self.object.tags.add(tag)
    #     return response


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
            Q(name__contains=q)
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
#
# def tag_page(request, slug):
#
#     tag = Tag.objects.get(slug=slug)
#     post_list =tag.post_set.all()  # Post.objects.filter(tags=tag)
#
#     return render(request, 'blog/post_list.html',{
#
#         'post_list' : post_list,
#         'categories' : Category.objects.all(),
#         'no_category_post_count' : Product.objects.filter(category=None).count(),
#         'tag' : tag
#     })

#
# def product_in_category(request, category_slug=None):
#     current_category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available_display=True)
#     if category_slug:
#         current_category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=current_category)
#     return render(request, 'product/product_list.html',
#                   {
#                       'current_category':current_category,
#                       'categories':categories,
#                       'products':products
#                   })
#


# def product_detail(request, pk, product_slug=None):
#     product = get_object_or_404(Product, pk=pk, slug=product_slug)
#     return render(request, 'product/product_detail.html', {'product':product})
