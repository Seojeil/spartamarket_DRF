from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Product, Category
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer
    )


class ProductAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        category_data = request.data.get('category')
        category = get_object_or_404(Category, category=category_data)
        request.data['category'] = category.pk
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductSearchAPIView(APIView):
    def get(self, request):
        search_type = request.data.get("search_type") # 프론트에서 입력값을 제한해야함
        search = request.data.get("search")
        if search_type == 'content':
            products = Product.objects.filter(
                content__contains=search)
        elif  search_type == 'title':
            products = Product.objects.filter(
                title__contains=search)
        elif search_type == 'title_content':
            products = Product.objects.filter(
                Q(title__contains=search) |
                Q(content__contains=search)
                )
        elif search_type == 'username':
            User = get_user_model()  # 회원명이 필요하기 때문에 유저모델을 호출
            try:  # 검색한 데이터와 일치하는 유저명을 호출
                author = User.objects.get(username=search)
            except User.DoesNotExist:  # 유저가 존재하지 않을 경우 빈 쿼리 반환
                products = Product.objects.none()
            else:  # 유저가 존재할 경우 해당 유저 필터링
                products = Product.objects.filter(
                    author=author)
        elif search_type == 'category':
            category = get_object_or_404(Category, category=search)
            products = Product.objects.filter(category=category.pk)
        else:
            products = Product.objects.all()
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
            return Response({"detail": "좋아요가 취소되었습니다."}, status=status.HTTP_200_OK)
        else:
            product.like_users.add(request.user)
            product.save()
            return Response({"detail": "이 상품이 좋아요!"}, status=status.HTTP_200_OK)


    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        
        if product.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        category_data = request.data.get('category')
        category = get_object_or_404(Category, category=category_data)
        request.data['category'] = category.pk
        
        serializer = ProductDetailSerializer(product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "존재하지 않는 글입니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if product.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        product.delete()
        return Response({"detail": "게시글이 삭제되었습니다.."}, status=status.HTTP_204_NO_CONTENT)