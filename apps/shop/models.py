from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from apps.common.models import BaseModel
from .manager import UserManager


class User(AbstractUser, BaseModel):
    fullname = models.CharField(_('Fullname'), max_length=55)
    phone_number = models.CharField(_('Phone_number'), max_length=20, unique=True)
    telegram_id = models.BigIntegerField(_('Telegram_id'), unique=True)
    language = models.CharField(_('Language'), max_length=17, default='uz')
    username = None
    first_name = None
    last_name = None
    email = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['telegram_id']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.fullname if self.fullname else self.phone_number


class Category(BaseModel):
    name_uz = models.CharField(max_length=55)
    name_ru = models.CharField(max_length=55)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children'
                               )

    objects = models.Manager()

    def __str__(self):
        return self.name_uz


    def get_name(self, language='uz'):
        return self.name_ru if language == 'ru' else self.name_uz

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(BaseModel):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    categories = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    main_image = models.ImageField(upload_to='products/main/')

    objects = models.Manager()

    def __str__(self):
        return self.name_uz

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ColorVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()

    def __str__(self):
        return f"{self.product.name_uz} - {self.color_name}"    # noqa

    class Meta:
        verbose_name = 'ColorVariant'
        verbose_name_plural = 'ColorVariants'


class ProductImage(models.Model):
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/colors/')

    objects = models.Manager()

    def __str__(self):
        return f"Image for {self.color_variant}"

    class Meta:
        verbose_name = 'ProductImage'
        verbose_name_plural = 'ProductImages'
