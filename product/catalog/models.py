from django.db import models
from django.contrib.auth.models import User
import random


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    stars = models.PositiveSmallIntegerField(
        default=1,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Рейтинг от 1 до 5"
    )

    def __str__(self):
        return f"Review for {self.product.title} - {self.stars}★"


def generate_code():
    return str(random.randint(100000, 999999))


class UserConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=6, default=generate_code)

    def __str__(self):
        return f"{self.user.username} — {self.code}"
