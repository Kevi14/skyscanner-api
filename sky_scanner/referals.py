from .models import *

class ReferralRewardSystem:
    DIRECT_REFERRAL_POINTS = 10
    SUB_REFERRAL_POINTS = 2
    POINTS_FOR_MAX_DISCOUNT = 500  # Example: 500 points needed for a 50% discount

    def __init__(self, user):
        self.user = user

    def calculate_points(self):
        # Fetch direct referrals
        direct_referrals = Referral.objects.filter(referrer=self.user).count()

        # Fetch sub-referrals
        sub_referrals = Referral.objects.filter(referrer__in=[ref.referred for ref in Referral.objects.filter(referrer=self.user)]).count()

        # Calculate total points
        total_points = (direct_referrals * self.DIRECT_REFERRAL_POINTS) + (sub_referrals * self.SUB_REFERRAL_POINTS)
        return total_points

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
            "discount_percentage": discount
        }
