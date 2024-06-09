from decimal import Decimal
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ValidationError


class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, password=None, username=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		if not username:
			raise ValueError('A username is required.')
		user = self.create_user(email, password)
		user.is_staff = True
		user.is_superuser = True
		user.username = username
		user.save()
		return user


class AppUser(AbstractBaseUser, PermissionsMixin):
	user_id = models.AutoField(primary_key=True)
	email = models.EmailField(max_length=50, unique=True)
	username = models.CharField(max_length=50)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	objects = AppUserManager()

	class Meta:
		verbose_name = ('Пользователь')
		verbose_name_plural = ('Пользователи')

	def __str__(self):
		return self.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/category_images/', null=True, blank=True)

    class Meta:
        verbose_name = ('Категория')
        verbose_name_plural = ('Категории')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(
		max_length=50,
        verbose_name=('Название'),
    )
    description = models.TextField(
		max_length=800,
        blank=True,
        verbose_name=('Описание'),
	)
    composition = models.TextField(
		max_length=400,
        blank=True,
        verbose_name=('Состав'),
	)
    discount = models.PositiveIntegerField(
        blank=True,
        verbose_name=('Скидка'),
        default=0,
        validators=[MaxValueValidator(100)]
    )
    quantity = models.PositiveIntegerField(
        blank=True,
        verbose_name=('Количество'),
    )
    weight = models.FloatField(
		blank=True,
        verbose_name=('Вес'),
	)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=('Цена'),
        validators=(
            MinValueValidator(Decimal('0.00')),
        ),
    )
    manufacture_date = models.DateField(
		blank=True,
        verbose_name=('Дата изготовления'),
	)
    expiry_date = models.DateField(
		blank=True,
        verbose_name=('Срок хранения'),
	)
    photos = models.ImageField(
        upload_to='media/product_photos/', 
        blank=True, null=True,
        verbose_name=('Блок фотографий'),
    )
    seller = models.ForeignKey(
        AppUser, 
        on_delete=models.CASCADE, 
        verbose_name=('Магазин')
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name=('Категория'),
    )

    class Meta:
        verbose_name = ('Продукт')
        verbose_name_plural = ('Продукты')

    def __str__(self) -> str:
        return self.name

    def price_with_discount(self) -> float:
        return self.price * (100 - self.discount) / 100

    price_with_discount.short_description = 'Цена со скидкой'
    
class Order(models.Model):
    date_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=('Дата и время')
    )
    buyer = models.ForeignKey(
        AppUser, 
        on_delete=models.CASCADE, 
        verbose_name=('Покупатель'),
        related_name='orders_as_buyer'
    )
    seller = models.ForeignKey(
        AppUser, 
        on_delete=models.CASCADE, 
        verbose_name=('Продавец'),
        related_name='orders_as_seller'
    )

    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name=('Продукт')
    )
    
    quantity = models.PositiveIntegerField(
        verbose_name=('Количество'),
        default=1
    )

    def clean(self):
        super().clean()
        if self.quantity > self.product.stock:
            raise ValidationError("Недостаточное количество товара на складе")
    
    def total_amount(self):
        total = 0
        for item in self.items.all():
            total += item.product.price_with_discount * item.quantity
        return total
    
    class Meta:
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')
        
class Cart(models.Model):
    user = models.ForeignKey(
        AppUser, 
        on_delete=models.CASCADE, 
        verbose_name=('Пользователь')
    )
        
    products = models.ManyToManyField(
        Product, 
        through='CartItem', 
        verbose_name=('Продукты')
    )
    
    class Meta:
        verbose_name = ('Корзина')
        verbose_name_plural = ('Корзины')

class CartItem(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name=('Продукт')
    )
        
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        verbose_name=('Корзина')
    )
        
    quantity = models.PositiveIntegerField(
        verbose_name=('Количество')
    )
    
    class Meta:
        verbose_name = ('Элемент корзины')
        verbose_name_plural = ('Элементы корзины')
