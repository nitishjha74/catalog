from django.urls import path
from catalog.views import business

urlpatterns = [
    # List all categories or create a new one
    path('categories/', business.CategoryListCreateView.as_view(), name='category-list-create'),
    # Retrieve, update, or delete a category by its 4-digit category_id
    path('categories/<int:category_id>/', business.CategoryDetailView.as_view(), name='category-detail'),

]
