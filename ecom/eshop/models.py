from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Sum
from django_countries.fields import CountryField

from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Sub_category(models.Model):
    sub_category_name=models.CharField(max_length=50)
    sub_category_image=models.ImageField(upload_to='documents')

    slug=models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("shop", kwargs={'slug': self.slug})


    def __str__(self):
        return self.sub_category_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(Sub_category, self).save(*args, **kwargs)

class Brands(models.Model):
    Brand_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    def __str__(self):
        return self.Brand_name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(Brands, self).save(*args, **kwargs)
class Product(models.Model):
    product_title=models.CharField(max_length=200)
    product_original_price=models.IntegerField()
    product_discounted_price=models.IntegerField()
    product_image_1=models.ImageField(upload_to='documents')
    product_image_2=models.ImageField(upload_to='documents')
    product_image_3=models.ImageField(upload_to='documents')
    product_discription=models.TextField(max_length=500)

    product_sub_category=models.ManyToManyField(Sub_category,blank=True,default='')
    product_brand=models.ManyToManyField(Brands,blank=True,default='')

    slug=models.SlugField(unique=True)
    def __str__(self):
        return self.product_title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(Product, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })


    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.product_title}"

    def get_total_item_price(self):
        return self.quantity * self.item.product_original_price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.product_discounted_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.product_discounted_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)

    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    def get_grand_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()+2
        if self.coupon:
            total -= self.coupon.amount
        return total

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'




class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)
post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)
