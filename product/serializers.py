from http import server
from rest_framework import serializers
from .models import Address, Category, Coupon, Order, Product, ProductImage, ProductItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'parent',
            'title',
            'slug',
            'text',
        ]


class CouponSerializer(serializers.Serializer):
    order_pk = serializers.CharField()
    key = serializers.CharField()



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['__all__']
        read_only_fields = ['__all__']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'slug',
            'product_code',
            'price',
            'about',
            'category',
            'seller',
            'discount_percent',
            'date_created',
            'date_updated',
        ]
        read_only_fields = ['product_code', 'seller', 'date_created']



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'product',
            'image',
        ]



class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = [
            'product',
            'user',
            'quantity',
            'date_created',
            'ordered',
        ]


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'user',
            'ostan',
            'city',
            'street',
            'palak',
            'full_address_type',
            'zip_code',
        ]
        read_only_fields = ['user']
