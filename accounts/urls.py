from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.SignupAPIView.as_view())
]