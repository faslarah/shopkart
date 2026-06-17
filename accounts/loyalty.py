def award_points(user, order_total):
    from accounts.models import Profile
    profile, _ = Profile.objects.get_or_create(user=user)
    earned = int(order_total) // 25  # ₹25 = 1 point, so ₹50 = 2 points
    profile.points += earned
    profile.save()
    return earned

def redeem_points(user, points_to_use):
    from accounts.models import Profile
    profile, _ = Profile.objects.get_or_create(user=user)
    if profile.points >= points_to_use:
        discount = points_to_use / 10
        profile.points -= points_to_use
        profile.points_redeemed += points_to_use
        profile.save()
        return discount
    return 0