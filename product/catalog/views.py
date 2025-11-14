from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.models import Avg, Count

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    RegisterSerializer,
    LoginSerializer,
    ConfirmSerializer
)

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer



class ProductReviewsListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.annotate(rating=Avg('reviews__stars'))


class CategoryWithCountListView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(products_count=Count('products'))



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})



class ConfirmUserView(generics.GenericAPIView):
    serializer_class = ConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Аккаунт подтверждён!"})
