from django.db import models
from django.contrib.auth.models import AbstractUser


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    def __str__(self):
        return f"Категория {self.name}"


class Product(models.Model):
    TYPE_CHOICES = (
        ('T48', 'Тетради 48 листов'),
        ('T24', 'Тетради 24 листа'),
        ('T96', 'Тетради 96 листов'),
        ('H', 'Ручки шариковые'),
        ('G', 'Ручки гелевые'),
        ('B', 'Бумага'),
    )
    type = models.CharField(max_length= 3, choices= TYPE_CHOICES, verbose_name="Тип товара")
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")
    price = models.PositiveIntegerField(default=0, verbose_name="Цена")
    category = models.ManyToManyField(Category,verbose_name="Категории")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="media", verbose_name="Картинка")
    is_new = models.BooleanField(default=False,verbose_name="Новинка")


    def __str__(self):
        return f"Товар {self.name} Цена {self.price} "


class Polzovatel(AbstractUser):
    phonenumber = models.CharField(max_length=14,null=True)


class Basket(models.Model):
    user = models.ForeignKey(Polzovatel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Товар {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f'OrderItem for {self.product.name}'


class Order(models.Model):
    user = models.ForeignKey(Polzovatel, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

        def __str__(self):
            return f'Order for {self.user.username}'

