from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass


class Product(models.Model):
    title=models.CharField(max_length=64)
    desc=models.CharField(max_length=300)
    base_price=models.IntegerField()
    price=models.IntegerField()
    photo=models.CharField(max_length=100)
    user=models.ForeignKey(User, on_delete=CASCADE, related_name="product")

    def __str__(self):
        return f"{self.title}  worth rs.{self.price}  by  {self.user}"

class Bid(models.Model):
    price=models.IntegerField()
    product=models.ForeignKey(Product,  on_delete=CASCADE,related_name="product_bid")
    user=models.ForeignKey(User, on_delete=CASCADE,  related_name="user_bid")

    def __str__(self):
        return f"{self.product}  bid by  {self.user}  at a rate of  {self.price}"

class Comment(models.Model):
    comment=models.CharField(max_length=300)
    product=models.ForeignKey(Product, on_delete=CASCADE, related_name="product_comm")
    user=models.ForeignKey(User, on_delete=CASCADE , related_name="user_comm")

    def __str__(self):
        return f"Comment by {self.user} on  {self.product} : {self.comment}"