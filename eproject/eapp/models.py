from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES=[
        (1,"mobile"),
        (2,"shoes"),
        (3,"clothes")
    ]
    name=models.CharField(max_length=100)
    price=models.FloatField()
    pdetails=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    category=models.IntegerField(choices=CATEGORY_CHOICES)
    image=models.ImageField(upload_to="images")
    def __str__(self):
        return self.name
    

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete = models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete =models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default = 1)
 
class Order(models.Model):
    order_id=models.CharField(max_length=100)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return self.order_id