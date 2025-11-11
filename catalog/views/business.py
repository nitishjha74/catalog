from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from catalog.serializers import business as business_serializers
from catalog.services.business import CategoryService
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
