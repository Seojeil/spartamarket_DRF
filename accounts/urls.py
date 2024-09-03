from django.urls import path
from accounts import views


urlpatterns = [
    path('', views.SignupAPIView.as_view()),
    path('login/', views.CustomTokenObtainPairView.as_view()),
    path('<str:username>/', views.ProfileAPIView.as_view()),
]