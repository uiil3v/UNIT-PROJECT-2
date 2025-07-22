from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path('products/', views.products_view, name="products_view"),
    path('detail/<int:product_id>/', views.detail_view, name="detail_view"),

    path('add/', views.add_view, name="add_view"),
    path('update/<int:product_id>/', views.update_view, name="update_view"),
    path('delete/<int:product_id>/', views.delete_view, name="delete_view"),
]
