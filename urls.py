from django.urls import path
from catalog.views import business

urlpatterns = [
    # Category endpoints
    path('categories/', business.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:category_id>/', business.CategoryDetailView.as_view(), name='category-detail'),
    
    # Product endpoints
    path('products/', business.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:product_id>/', business.ProductDetailView.as_view(), name='product-detail'),
]