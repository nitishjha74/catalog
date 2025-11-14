from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from catalog.serializers import business as business_serializers
from catalog.services.business import CategoryService, ProductService
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from catalog.authentication.business import SSOBusinessTokenAuthentication



# ---------- Category List + Create ----------



class CategoryListCreateView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List all categories",
        operation_description="Retrieve all active categories created by the authenticated merchant.",
        responses={200: business_serializers.CategorySerializer(many=True)},
    )
    def get(self, request):
        business_id = request.user.business_id
        categories = CategoryService.get_all(business_id)
        serializer = business_serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new category",
        operation_description="Create a new category for the authenticated merchant. The business_id is automatically assigned from the logged-in user.",
        request_body=business_serializers.CategorySerializer,
        responses={
            201: business_serializers.CategorySerializer(),
            400: "Invalid data or missing fields"
        },
        examples={
            "application/json": {
                "name": "Electronics",
                "slug": "electronics",
                "image_url": "https://s3.amazonaws.com/jsjcard/electronics.jpg",
                "description": "All types of electronic gadgets"
            }
        },
    )
    def post(self, request):
        business_id = request.user.business_id
        serializer = business_serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = CategoryService.create(serializer.validated_data, business_id)
            return Response(business_serializers.CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ---------- Category Detail (GET, PUT, DELETE) ----------



class CategoryDetailView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a single category",
        operation_description="Fetch details of a specific category by category_id belonging to the logged-in merchant.",
        manual_parameters=[
            openapi.Parameter("category_id", openapi.IN_PATH, description="4-digit Category ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: business_serializers.CategorySerializer()},
    )
    def get(self, request, category_id):
        business_id = request.user.business_id
        category = CategoryService.get_by_id(category_id, business_id)
        serializer = business_serializers.CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a category",
        operation_description="Update category details such as name, slug, image_url, or description.",
        manual_parameters=[
            openapi.Parameter("category_id", openapi.IN_PATH, description="4-digit Category ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=business_serializers.CategorySerializer,
        responses={
            200: business_serializers.CategorySerializer(),
            400: "Invalid data"
        },
        examples={
            "application/json": {
                "name": "Updated Category Name",
                "description": "Updated description for the category."
            }
        },
    )
    def put(self, request, category_id):
        business_id = request.user.business_id
        serializer = business_serializers.CategorySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            category = CategoryService.update(category_id, business_id, serializer.validated_data)
            return Response(business_serializers.CategorySerializer(category).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a category",
        operation_description="Delete a category by its category_id belonging to the authenticated merchant.",
        manual_parameters=[
            openapi.Parameter("category_id", openapi.IN_PATH, description="4-digit Category ID", type=openapi.TYPE_INTEGER)
        ],
        responses={204: "Category deleted successfully"},
    )
    def delete(self, request, category_id):
        business_id = request.user.business_id
        CategoryService.delete(category_id, business_id)
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# ---------- Products by Category ----------



class ProductsByCategoryView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get products by category",
        operation_description="Retrieve all products belonging to a specific category for the authenticated merchant.",
        manual_parameters=[
            openapi.Parameter(
                "category_id", 
                openapi.IN_PATH, 
                description="4-digit Category ID", 
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: business_serializers.ProductSerializer(many=True),
            404: "Category not found"
        },
    )
    def get(self, request, category_id):
        business_id = request.user.business_id
        
        # First verify the category exists and belongs to the business
        try:
            category = CategoryService.get_by_id(category_id, business_id)
        except:
            return Response(
                {"error": f"Category with ID {category_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get products for this category
        products = ProductService.get_products_by_category(category_id, business_id)
        serializer = business_serializers.ProductSerializer(products, many=True)
        
        # Include category info in response
        response_data = {
            "category_id": category_id,
            "category_name": category.name,
            "products_count": len(serializer.data),
            "products": serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)



# ---------- Product List + Create ----------



class ProductListCreateView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="Retrieve all active products created by the authenticated merchant.",
        responses={200: business_serializers.ProductSerializer(many=True)},
    )
    def get(self, request):
        business_id = request.user.business_id
        products = ProductService.get_all(business_id)
        serializer = business_serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="Create a new product for the authenticated merchant. The business_id is automatically assigned from the logged-in user.",
        request_body=business_serializers.ProductSerializer,
        responses={
            201: business_serializers.ProductSerializer(),
            400: "Invalid data or missing fields"
        },
        examples={
            "application/json": {
                "category": 1001,
                "name": "Smartphone",
                "description": "Latest smartphone with advanced features",
                "price": "19999.00",
                "image_url": "https://s3.amazonaws.com/jsjcard/smartphone.jpg",
                "is_feature": True
            }
        },
    )
    def post(self, request):
        business_id = request.user.business_id
        # Pass the request context to the serializer for business_id access
        serializer = business_serializers.ProductSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            try:
                # The serializer now handles category conversion and business_id assignment
                # Just call save() which will call serializer.create()
                product = serializer.save()
                return Response(
                    business_serializers.ProductSerializer(product).data, 
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                # Handle any unexpected errors
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------- Featured Products List ----------



class FeaturedProductsListView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List featured products",
        operation_description="Retrieve all featured products (is_feature=True) created by the authenticated merchant.",
        responses={200: business_serializers.ProductSerializer(many=True)},
    )
    def get(self, request):
        business_id = request.user.business_id
        featured_products = ProductService.get_featured_products(business_id)
        serializer = business_serializers.ProductSerializer(featured_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




# ---------- Product Detail (GET, PUT, PATCH, DELETE) ----------



class ProductDetailView(APIView):
    authentication_classes = [SSOBusinessTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a single product",
        operation_description="Fetch details of a specific product by product_id belonging to the logged-in merchant.",
        manual_parameters=[
            openapi.Parameter("product_id", openapi.IN_PATH, description="6-digit Product ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: business_serializers.ProductSerializer()},
    )
    def get(self, request, product_id):
        business_id = request.user.business_id
        product = ProductService.get_by_id(product_id, business_id)
        serializer = business_serializers.ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a product",
        operation_description="Update product details completely.",
        manual_parameters=[
            openapi.Parameter("product_id", openapi.IN_PATH, description="6-digit Product ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=business_serializers.ProductSerializer,
        responses={
            200: business_serializers.ProductSerializer(),
            400: "Invalid data"
        },
    )
    def put(self, request, product_id):
        business_id = request.user.business_id
        serializer = business_serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = ProductService.update(product_id, business_id, serializer.validated_data)
            return Response(business_serializers.ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial update a product",
        operation_description="Partially update product details.",
        manual_parameters=[
            openapi.Parameter("product_id", openapi.IN_PATH, description="6-digit Product ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=business_serializers.ProductSerializer,
        responses={
            200: business_serializers.ProductSerializer(),
            400: "Invalid data"
        },
    )
    def patch(self, request, product_id):
        business_id = request.user.business_id
        serializer = business_serializers.ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            product = ProductService.update(product_id, business_id, serializer.validated_data)
            return Response(business_serializers.ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a product",
        operation_description="Delete a product by its product_id belonging to the authenticated merchant.",
        manual_parameters=[
            openapi.Parameter("product_id", openapi.IN_PATH, description="6-digit Product ID", type=openapi.TYPE_INTEGER)
        ],
        responses={204: "Product deleted successfully"},
    )
    def delete(self, request, product_id):
        business_id = request.user.business_id
        ProductService.delete(product_id, business_id)
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)