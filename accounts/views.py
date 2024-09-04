from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .serializers import (
    SignupSerializer,
    ProfileSerializer
    )
from datetime import datetime


User = get_user_model()

class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(permission_classes([IsAuthenticated]))
    def delete(self, request):
        account = User.objects.get(pk=request.user.pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "아이디/비밀번호를 다시확인해주세요.",
        "already_logged_in": "이미 로그인된 상태입니다.",
    }


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        refresh_token  = request.data.get("refresh")
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception  as e:
            return Response({"error": "이미 만료되었거나 잘못된 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        user = User.objects.get(username=username)
        account = User.objects.get(pk=user.id)
        serializer = ProfileSerializer(account)
        return Response(serializer.data)