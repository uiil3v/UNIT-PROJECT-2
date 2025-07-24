from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Product 
from .forms import ProductForm
from django.core.paginator import Paginator
from django.db.models import Q



def products_view(request: HttpRequest):
    all_products = Product.objects.all()

    # فلترة البحث
    search_query = request.GET.get("search")
    if search_query:
        all_products = all_products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # فلترة التصنيف
    category_filter = request.GET.get("category")
    if category_filter:
        all_products = all_products.filter(category=category_filter)

    # ترتيب حسب السعر
    price_sort = request.GET.get("price")
    if price_sort == "low-high":
        all_products = all_products.order_by("price")
    elif price_sort == "high-low":
        all_products = all_products.order_by("-price")

    # الترقيم
    paginator = Paginator(all_products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "store/products.html", {"products": page_obj})

def detail_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    # منتجات مشابهة بنفس التصنيف
    relevant_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    # ما فيه تعليقات حالياً، لكن نجهز الكود لو حبيت تضيفه لاحقًا
    return render(request, "store/detail.html", {
        "product": product,
        "relevant_products": relevant_products
    })

def add_view(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("store:products_view")  # غيّرها لاسم مسارك الصحيح
    else:
        form = ProductForm()
    return render(request, "store/add.html", {"form": form})

def update_view(request: HttpRequest, product_id: int):
    return render(request, "store/update.html")

def delete_view(request: HttpRequest, product_id: int):
    return render(request, "store/delete.html")

