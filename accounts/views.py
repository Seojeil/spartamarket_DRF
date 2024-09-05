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
from django.shortcuts import get_object_or_404
from .serializers import (
    AccountSerializer,
    AccountUpdateSerializer,
    PasswordSerializer,
    )


User = get_user_model()

class SignupAPIView(APIView):
    # 회원가입
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 회원 탈퇴
    @method_decorator(permission_classes([IsAuthenticated]))
    def delete(self, request):
        password = request.data.get('password')
        account = request.user
        
        if not account.check_password(password):
            return Response({"detail": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        account.delete()
        return Response({"detail": "회원정보가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

# 로그인(토큰 생성)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "아이디/비밀번호를 다시확인해주세요.",
        "already_logged_in": "이미 로그인된 상태입니다.",
    }


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 로그아웃
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
    
    def get_object(self, username):
        return get_object_or_404(User, username=username)
    
    # 유저페이지 조회
    def get(self, request, username):
        user = self.get_object(username)
        account = User.objects.get(pk=user.id)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 팔로우
    def post(self, request, username):
        user = self.get_object(username)
        
        if user == request.user:
            return Response({"error": "자신을 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            return Response({"detail": "팔로우가 취소되었습니다."}, status=status.HTTP_200_OK)
        else:
            user.followers.add(request.user)
            return Response({"detail": "팔로우되었습니다."}, status=status.HTTP_200_OK)
    
    # 개인정보 수정
    def put(self, request, username):
        account = get_object_or_404(User, username=username)
        
        if account.pk == request.user.pk:
            serializer = AccountUpdateSerializer(account, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "일치하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 비밀번호 수정
    def put(self, request):
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"detail": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

