from datetime import datetime, timedelta
from .models import Booking

class Discount:
    TIER_DISCOUNTS = {
        'Bronze': {
            'range': (1, 4),
            'discounts': {
                'Economic': 5,
                'Business': 3,
                'First Class': 2
            }
        },
        'Silver': {
            'range': (5, 9),
            'discounts': {
                'Economic': 10,
                'Business': 7,
                'First Class': 5
            }
        },
        'Gold': {
            'range': (10, 19),
            'discounts': {
                'Economic': 15,
                'Business': 12,
                'First Class': 10
            }
        },
        'Platinum': {
            'range': (20, 29),
            'discounts': {
                'Economic': 20,
                'Business': 18,
                'First Class': 15
            }
        },
        'Diamond': {
            'range': (30, 10000),
            'discounts': {
                'Economic': 25,
                'Business': 22,
                'First Class': 20
            }
        }
    }
    def __init__(self, flights):
        self.flights = flights

    def get_tier_and_max_discount(self):
        for tier, details in self.TIER_DISCOUNTS.items():
            if details['range'][0] <= self.flights <= details['range'][1]:
                return tier, max(details['discounts'].values())
        return None, 0

class RewardSystem:
    def __init__(self, user):
        self.user = user

    def flights_this_year(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        bookings_count = Booking.objects.filter(user=self.user, tickets__issued_date__range=(start_date, end_date)).distinct().count()
        return bookings_count

    def get_discount(self):
        flight_count = self.flights_this_year()
        discount = Discount(flight_count)
        _, discount_value = discount.get_tier_and_max_discount()
        return discount_value

    def get_price_after_discount(self, original_price):
        discount = self.get_discount()
        return original_price - (original_price * discount / 100)

    def notify_user(self):
        discount = self.get_discount()
        if discount:
            message = f"Congratulations! You're eligible for a maximum discount of {discount}% on your next flight!"
            print(message)

    def get_discount_info(self):
        flight_count = self.flights_this_year()
        discount = Discount(flight_count)
        tier, discount_value = discount.get_tier_and_max_discount()

        # Including all tier details in the response
        all_tiers = []
        for t, details in Discount.TIER_DISCOUNTS.items():
            all_tiers.append({
                "tier_name": t,
                "flight_range": details['range'],
                "discounts": details['discounts']
            })

        return {
            "flights_this_year": flight_count,
            "current_tier": tier,
            "max_discount_percentage": discount_value,
            "all_tiers": all_tiers
        }
