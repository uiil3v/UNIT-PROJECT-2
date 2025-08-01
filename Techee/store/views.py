from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Product, Cart, CartItem
from .forms import ProductForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



def products_view(request: HttpRequest):
    all_products = Product.objects.all()
 

    search_query = request.GET.get("search")
    if search_query:
        all_products = all_products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    category_filter = request.GET.get("category")
    if category_filter:
        all_products = all_products.filter(category=category_filter)

    price_sort = request.GET.get("price")
    if price_sort == "low-high":
        all_products = all_products.order_by("price")
    elif price_sort == "high-low":
        all_products = all_products.order_by("-price")

    paginator = Paginator(all_products, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "store/products.html", {"products": page_obj})



def detail_view(request: HttpRequest, product_id: int):
    product = get_object_or_404(Product, id=product_id)
    relevant_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    comments = product.comments.order_by('-created_at')

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.user = request.user
                comment.save()
                return redirect('store:detail_view', product_id=product.id)
        else:
            return redirect('users:login_view')
    else:
        form = CommentForm()

    return render(request, "store/detail.html", {
        "product": product,
        "relevant_products": relevant_products,
        "comments": comments,
        "form": form,
    })

@user_passes_test(lambda u: u.is_staff)
def add_view(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect("store:products_view")
            except Exception as e:
                print("❌ Error during form.save():", e)  
                return render(request, "store/add.html", {
                    "form": form,
                    "error": f"Something went wrong: {str(e)}"
                })
        else:
            print("❌ Form validation errors:", form.errors)
            return render(request, "store/add.html", {
                "form": form,
                "error": "Form validation failed. Please check your inputs."
            })
    else:
        form = ProductForm()
    return render(request, "store/add.html", {"form": form})



@user_passes_test(lambda u: u.is_staff)
def update_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("store:products_view")
    else:
        form = ProductForm(instance=product)
    return render(request, "store/update.html", {"form": form, "product": product})


@user_passes_test(lambda u: u.is_staff)
def delete_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.delete()
    return redirect("store:products_view")



@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("store:cart_view")



@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        new_quantity = int(request.POST.get("quantity", 1))
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()

        return redirect("store:cart_view")

    cart_items = cart.items.select_related('product')

    items_with_subtotal = []
    total = 0

    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total += subtotal
        items_with_subtotal.append({
            "item": item,
            "subtotal": subtotal
        })

    return render(request, "store/cart.html", {
        "cart_items": items_with_subtotal,
        "total": total,
    })



@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect("store:cart_view")



@login_required
def clear_cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return redirect("store:cart_view")



@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product')

    items_with_subtotal = []
    total = 0
    for item in cart_items:
        subtotal = item.product.price * item.quantity
        total += subtotal
        items_with_subtotal.append({
            'item': item,
            'subtotal': subtotal,
        })

    if request.method == "POST":
        cart.items.all().delete()
        return redirect("store:thank_you_view")

    return render(request, "store/checkout.html", {
        'cart_items': items_with_subtotal,
        'total': total,
    })



@login_required
def thank_you_view(request):
    return render(request, "store/thank_you.html")