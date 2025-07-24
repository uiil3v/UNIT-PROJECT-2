from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Product 
from django.core.paginator import Paginator

def products_view(request: HttpRequest):
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 8)  
    page_number = request.GET.get("page") 
    page_obj = paginator.get_page(page_number)

    return render(request, "store/products.html", {"products": page_obj})

def detail_view(request: HttpRequest, product_id: int):
    return render(request, "store/detail.html")

def add_view(request: HttpRequest):
    return render(request, "store/add.html")

def update_view(request: HttpRequest, product_id: int):
    return render(request, "store/update.html")

def delete_view(request: HttpRequest, product_id: int):
    return render(request, "store/delete.html")

