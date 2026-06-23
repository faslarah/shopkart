from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    STATUS = [
        ('pending',    'Pending'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100)
    email           = models.EmailField()
    phone           = models.CharField(max_length=15)
    address         = models.TextField()
    city            = models.CharField(max_length=100)
    state           = models.CharField(max_length=100)
    pincode         = models.CharField(max_length=10)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    paid            = models.BooleanField(default=False)
    status          = models.CharField(max_length=20, choices=STATUS, default='pending')
    total_price     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points_redeemed = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Order #{self.id} by {self.user.username}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity