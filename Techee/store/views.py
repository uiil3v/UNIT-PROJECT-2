from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def products_view (request: HttpRequest):
    return render(request, "store/products.html")

def detail_view(request: HttpRequest, product_id: int):
    return render(request, "store/detail.html")

def add_view(request: HttpRequest):
    return render(request, "store/add.html")

def update_view(request: HttpRequest, product_id: int):
    return render(request, "store/update.html")

def delete_view(request: HttpRequest, product_id: int):
    return render(request, "store/delete.html")

