from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    phone   = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city    = models.CharField(max_length=100, blank=True)
    state   = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    avatar  = models.ImageField(upload_to='avatars/', blank=True)
    points = models.IntegerField(default=0)
    points_redeemed = models.IntegerField(default=0)  

    def __str__(self):
        return f'{self.user.username} Profile'


class Wishlist(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    added   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')