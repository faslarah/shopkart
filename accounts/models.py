from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    phone           = models.CharField(max_length=15, blank=True)
    address         = models.TextField(blank=True)
    city            = models.CharField(max_length=100, blank=True)
    state           = models.CharField(max_length=100, blank=True)
    pincode         = models.CharField(max_length=10, blank=True)
    avatar          = models.ImageField(upload_to='avatars/', blank=True)
    points          = models.IntegerField(default=0)
    points_redeemed = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'


class Wishlist(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    added   = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

class LoyaltySettings(models.Model):
    spend_amount        = models.PositiveIntegerField(default=1,   help_text='Amount spent in ₹ to earn points')
    points_per_spend    = models.PositiveIntegerField(default=1,   help_text='Points earned per spend amount')
    points_to_rupee     = models.PositiveIntegerField(default=100, help_text='Points needed for ₹10 discount')
    rupee_per_redeem    = models.PositiveIntegerField(default=10,  help_text='₹ discount per points_to_rupee points')
    min_redeem_points   = models.PositiveIntegerField(default=500, help_text='Minimum points to redeem')
    is_active           = models.BooleanField(default=True,        help_text='Enable/disable loyalty system')
    updated             = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Loyalty Settings'

    def __str__(self):
        return f'Loyalty Settings (updated {self.updated})'

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj