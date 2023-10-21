from datetime import datetime, timedelta
from .models import Booking

class Discount:
    ECONOMY_PRICE_THRESHOLD = 300  # Example value
    BUSINESS_PRICE_THRESHOLD = 700  # Example value

    def __init__(self, flights, price):
        self.flights = flights
        self.price = price

    def get_percentage(self):
        base_discount = 0
        if self.flights >= 2 and self.flights < 5:
            base_discount = 10
        elif self.flights >= 5 and self.flights < 10 and self.flights % 3 == 0:
            base_discount = 30
        elif self.flights == 10:
            base_discount = 60

        if self.price < self.ECONOMY_PRICE_THRESHOLD:
            return base_discount
        elif self.price < self.BUSINESS_PRICE_THRESHOLD:
            return base_discount + 5  # Additional 5% for Business
        else:
            return base_discount + 10  # Additional 10% for First Class

class RewardSystem:
    def __init__(self, user):
        self.user = user

    def flights_this_year(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
        bookings_count = Booking.objects.filter(user=self.user, tickets__issued_date__range=(start_date, end_date)).distinct().count()
        return bookings_count

    def get_discount(self, price):
        flight_count = self.flights_this_year()
        discount = Discount(flight_count, price)
        return discount.get_percentage()

    def get_price_after_discount(self, original_price):
        discount = self.get_discount(original_price)
        return original_price - (original_price * discount / 100)

    def notify_user(self, price):
        discount = self.get_discount(price)
        if discount:
            message = f"Congratulations! You're eligible for a {discount}% discount on your next flight!"
            print(message)

    def get_discount_info(self, price):
        flight_count = self.flights_this_year()
        discount = self.get_discount(price)
        return {
            "flights_this_year": flight_count,
            "discount_percentage": discount
        }
