from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Product, Coupon, Order, Category, ProductItem
from .serializers import (
    CategorySerializer, 
    CouponSerializer, 
    OrderSerializer, 
    ProductSerializer, 
    CheckoutSerializer, 
    ProductItemSerializer
)
from .permissions import (
    IsSelfOr404, 
    IsSelfOrReadOnlyObject, 
    IsSuperUserOrReadOnly, 
    IsSellerOrReadOnly
)



# Create your views here.
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')
    permission_classes = [IsSellerOrReadOnly | IsSuperUserOrReadOnly]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, 
                        context={'author': request.user}, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-id')
    permission_classes = [IsSellerOrReadOnly | IsSuperUserOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.author = request.user
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED, headers=headers)



class OrderRetrieve(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsSelfOrReadOnlyObject | IsSuperUserOrReadOnly]

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
    


class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-id')
    permission_classes = [IsSelfOrReadOnlyObject | IsSuperUserOrReadOnly]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-id')



class CouponView(generics.GenericAPIView):
    def post(self, request):
        serializer = CouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data.get('key')
        order_pk = int(serializer.validated_data.get('order_pk'))
        try:
            coupon = Coupon.objects.get(key=key)
            order = Order.objects.get(pk=order_pk)
            order.coupon = coupon
            order.save()
            o_serializer = OrderSerializer(data=order)
            return Response(o_serializer, status=status.HTTP_200_OK)

        except Coupon.DoesNotExist:
            return Response({
                'NotFoundError': 'Coupon Not Found.'
            }, status=status.HTTP_404_NOT_FOUND)



class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id').order_by('-parent')
    permission_classes = [IsSuperUserOrReadOnly]

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.kwargs.get('pk'))
    


class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-id').order_by('-parent')
    permission_classes = [IsSuperUserOrReadOnly]



class ProductItems(generics.RetrieveAPIView):
    serializer_class = ProductItemSerializer
    queryset = ProductItem.objects.all()
    permission_classes = [IsSelfOrReadOnlyObject | IsSuperUserOrReadOnly]

    def get_queryset(self):
        return ProductItem.objects.filter(user=self.request.user)



class CheckoutView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsSelfOr404]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.author = request.user
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, 
                    status=status.HTTP_201_CREATED, headers=headers)
