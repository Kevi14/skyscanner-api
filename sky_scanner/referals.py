from custom_auth.models import ReferralCode,Referral
import random
import string
from datetime import timedelta, date
from .models import PromoCode
from django.db.models import Sum

class ReferralRewardSystem:
    DIRECT_REFERRAL_POINTS = 10
    SUB_REFERRAL_POINTS = 2
    POINTS_FOR_MAX_DISCOUNT = 500  # Example: 500 points needed for a 50% discount

    def __init__(self, user):
        self.user = user

    def get_discount_percentage(self):
        # Calculate discount based on total points
        total_points = self.calculate_points()

        # Calculate discount: for simplicity, let's say for every 10 points, user gets 1% discount
        discount_percentage = (total_points / self.POINTS_FOR_MAX_DISCOUNT) * 50
        return min(discount_percentage, 50)  # Max discount is 50%

    def notify_user(self):
        discount = self.get_discount_percentage()
        if discount:
            message = f"Congratulations! You've earned a {discount:.2f}% discount thanks to your referrals!"
            print(message)
    def get_reward_info(self):
        total_points = self.calculate_points()
        discount = self.get_discount_percentage()
        return {
            "total_points": total_points,
            "discount_percentage": discount,
            "max_points":self.POINTS_FOR_MAX_DISCOUNT,
        }
    def calculate_points(self):
        # Fetch direct referrals
        direct_referrals = Referral.objects.filter(referrer=self.user).count()

        # Fetch sub-referrals
        sub_referrals = Referral.objects.filter(referrer__in=[ref.referred for ref in Referral.objects.filter(referrer=self.user)]).count()

        # Calculate total points
        total_points = (direct_referrals * self.DIRECT_REFERRAL_POINTS) + (sub_referrals * self.SUB_REFERRAL_POINTS)

        # Deduct points that have been used in promo codes
        consumed_points = self.calculate_consumed_points()
        remaining_points = total_points - consumed_points

        return max(remaining_points, 0)  # Ensure points don't go negative

    def calculate_consumed_points(self):
    # Get the total points consumed by the user via promo codes
        return PromoCode.objects.filter(user=self.user).aggregate(total=Sum('points_consumed'))['total'] or 0

    def generate_promo_code(self):
        total_points = self.calculate_points()
        
        # Random code generation
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        validity_duration = 30  # Promo code validity in days
        validity_date = date.today() + timedelta(days=validity_duration)

        promo_code = PromoCode.objects.create(
            user=self.user,
            code=code,
            validity=validity_date,
            points_consumed=total_points
        )
        
        # Return promo code details
        return {
            "promo_code": code,
            "validity_date": validity_date
        }
