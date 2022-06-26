from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),#name es como la voy a referenciar desde el Templar, por ej para hacer links: {% url 'store' %}
    path('<slug:category_slug>/', views.store, name="products_by_category"),#path dinamico
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail"),#path dinamico
]
