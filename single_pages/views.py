from django.shortcuts import render

# Create your views here.

def landing(request):
    return render(request, 'single_pages/landing.html')

def mypage(request):
    return render(request, 'single_pages/mypage.html')

def about(request):
    return render(request, 'single_pages/about.html')

