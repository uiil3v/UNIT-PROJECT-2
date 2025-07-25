from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path('products/', views.products_view, name="products_view"),
    path('detail/<int:product_id>/', views.detail_view, name="detail_view"),

    path('add/', views.add_view, name="add_view"),
    path('update/<int:product_id>/', views.update_view, name="update_view"),
    path('delete/<int:product_id>/', views.delete_view, name="delete_view"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name="add_to_cart_view"),
    path('cart/', views.cart_view, name="cart_view"),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart_view, name="remove_from_cart_view"),
    path("clear-cart/", views.clear_cart_view, name="clear_cart_view"),
    path('checkout/', views.checkout_view, name="checkout_view"),
    path('thank-you/', views.thank_you_view, name="thank_you_view"),
]
