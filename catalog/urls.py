from django.urls import path
from catalog.views.business import (
    CategoryListCreateView, 
    CategoryDetailView, 
    ProductListCreateView, 
    ProductDetailView,
    FeaturedProductsListView,
    ProductsByCategoryView
)

urlpatterns = [
    # Category endpoints
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:category_id>/products/', ProductsByCategoryView.as_view(), name='products-by-category'),
    
    # Product endpoints
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/featured/', FeaturedProductsListView.as_view(), name='featured-products-list'),
]