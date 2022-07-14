from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.conf import settings
from django.db import models
from payment.models import Payment


# Create your models here.
class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product/images/')

    def __str__(self):
        return self.product.title


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)
    text = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=25, unique=True)
    product_code = models.UUIDField(default=uuid4, unique=True)
    price = models.FloatField()
    about = models.TextField(max_length=500)
    category = models.ManyToManyField(Category)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    discount_percent = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_created=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    ref_code = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    date_ordered = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address',
        on_delete=models.CASCADE
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE
    )
    coupon = models.ForeignKey(
        'Coupon',
        on_delete=models.CASCADE
    )
    delivered = models.BooleanField(default=False)
    notif_recieved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    title = models.CharField(max_length=100)
    code = models.UUIDField(default=uuid4, unique=True)
    discount_price = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class User(AbstractUser): 
    profile = models.ImageField(upload_to='user/pics/')
    phone_number = models.CharField(max_length=11)
    is_seller = models.BooleanField(default=False)
    is_post_author = models.BooleanField(default=False)
    is_supporter = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username


class Address(models.Model):
    user = models.ForeignKey(User, 
                on_delete=models.CASCADE, related_name='addresses')
    ostan = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    palak = models.CharField(max_length=100)
    full_address_type = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=100)

    def __str__(self):
        return 'Address for ' + self.user.username
