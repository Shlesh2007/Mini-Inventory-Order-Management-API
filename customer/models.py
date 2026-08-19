from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50,unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CANCELLED = "CANCELLED", "Cancelled"
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="orders")
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    total = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    subtotal = models.DecimalField(max_digits=12,decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"