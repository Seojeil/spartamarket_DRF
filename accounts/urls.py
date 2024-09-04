from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', views.SignupAPIView.as_view()),
    path('login/', views.CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view()),
    path('<str:username>/', views.ProfileAPIView.as_view()),
]