from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('categories/with-count/', views.CategoryWithCountListView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view()),

    path('products/', views.ProductListView.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    path('products/reviews/', views.ProductReviewsListView.as_view()),

    path('reviews/', views.ReviewListView.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view()),

    path('users/register/', views.RegisterView.as_view()),
    path('users/login/', views.LoginView.as_view()),
    path('users/confirm/', views.ConfirmUserView.as_view()),
]

