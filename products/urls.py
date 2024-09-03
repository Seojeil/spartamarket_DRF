from django.urls import path
from products import views

urlpatterns = [
    path('', views.ProductAPIView.as_view()),
    path('<int:pk>/', views.ProductDetailAPIView.as_view()),
]