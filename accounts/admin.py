from django.contrib import admin
from .models import Profile, Wishlist, LoyaltySettings

admin.site.register(Profile)
admin.site.register(Wishlist)

@admin.register(LoyaltySettings)
class LoyaltySettingsAdmin(admin.ModelAdmin):
    list_display = ['spend_amount', 'points_per_spend', 'points_to_rupee', 'min_redeem_points', 'is_active']