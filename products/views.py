from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import Product, Category, Tag
from .serializers import (
    ProductSerializer,
    ProductDetailSerializer
    )


class ProductAPIView(APIView):
    # 게시글 목록
    def get(self, request):
        sort = request.data.get('sort') # 프론트에서 입력값 제한
        
        if sort == 'like':
            products = Product.objects.annotate(
                like_count=Count('like_users')
                ).order_by('-like_count', '-created_at')
        else:
            products = Product.objects.all().order_by('-created_at')
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 작성
    @method_decorator(permission_classes([IsAuthenticated]))
    def post(self, request):
        request.data['category'] = get_category_pk(request)
        
        tags = request.data.get('tags') # 프론트에서 입력값 제한
        tag_instances = []
        
        if tags:
            append_tags(tags, tag_instances)
            
        request.data['tags'] = tag_instances
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductSearchAPIView(APIView):
    # 게시글 검색
    def get(self, request):
        search_type = request.data.get("search_type") # 프론트에서 입력값을 제한해야함
        search = request.data.get("search")
        
        if search_type == 'content':
            products = Product.objects.filter(
                content__contains=search).order_by('-created_at')
            
        elif  search_type == 'title':
            products = Product.objects.filter(
                title__contains=search).order_by('-created_at')
            
        elif search_type == 'title_content':
            products = Product.objects.filter(
                Q(title__contains=search) |
                Q(content__contains=search)
                ).order_by('-created_at')
            
        elif search_type == 'username':
            author = get_object_or_404(get_user_model(), username=search)
            products = Product.objects.filter(author=author).order_by('-created_at')
            
        elif search_type == 'category':
            category = get_object_or_404(Category, category=search)
            products = Product.objects.filter(category=category.pk).order_by('-created_at')
        
        elif search_type == 'tags':
            search = search.upper()
            tag = get_object_or_404(Tag, name=search)
            products = Product.objects.filter(tags=tag.pk).order_by('-created_at')
        
        else:
            products = Product.objects.all().order_by('-created_at')
        
        serializer = ProductSerializer(products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)
    
    # 게시글 상세페이지 조회
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 좋아요
    def post(self, request, pk):
        product = self.get_object(pk)
        
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
            return Response({"detail": "좋아요가 취소되었습니다."}, status=status.HTTP_200_OK)
        else:
            product.like_users.add(request.user)
            product.save()
            return Response({"detail": "이 상품이 좋아요!"}, status=status.HTTP_200_OK)

    # 게시글 수정
    def put(self, request, pk):
        product = self.get_object(pk)
        
        if product.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        request.data['category'] = get_category_pk(request)
        product.tags.clear()
        
        tags = request.data.get('tags') # 프론트에서 입력값 제한
        tag_instances = []
        
        if tags:
            append_tags(tags, tag_instances)
        
        request.data['tags'] = tag_instances
        serializer = ProductDetailSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    #게시글 삭제
    def delete(self, request, pk):
        product = self.get_object(pk)
        
        if product.author != request.user:
            return Response({"error": "작성자가 일치하지 않습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        product.delete()
        return Response({"detail": "게시글이 삭제되었습니다.."}, status=status.HTTP_204_NO_CONTENT)


# 글작성/수정에 포함되는 카테고리 추가 함수
def get_category_pk(request):
    category_data = request.data.get('category')
    category = get_object_or_404(Category, category=category_data)
    return category.pk


# 글작성/수정에 포함되는 태그 추가 함수
def append_tags(tags, tag_instances):
    if isinstance(tags, str):
        tags = tags.split(',')
    
    for tag in tags:
        tag = tag.upper()
        if tag:
            tag_instance, created = Tag.objects.get_or_create(name=tag)
            tag_instances.append(tag_instance.pk)
    return tag_instances