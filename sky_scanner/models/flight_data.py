from django.db import models
from .reference_data import IATACode,FlightNumber,AirlineCode,BookingClass
from django.core.validators import MinValueValidator, MaxValueValidator

class Flight(models.Model):
    flight_number = models.CharField(max_length=6)
    origin = models.ForeignKey(IATACode, related_name='departure_flights', on_delete=models.CASCADE)
    destination = models.ForeignKey(IATACode, related_name='arrival_flights', on_delete=models.CASCADE)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Adding the price field

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

# Contact Model
class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

# BookedSegment Model
class BookedSegment(models.Model):
    origin = models.ForeignKey(IATACode, related_name='departure_airports', on_delete=models.CASCADE)
    destination = models.ForeignKey(IATACode, related_name='arrival_airports', on_delete=models.CASCADE)
    flight_number = models.ForeignKey(FlightNumber, on_delete=models.CASCADE)
    flight_Date = models.DateField()
    airline_code = models.ForeignKey(AirlineCode, on_delete=models.CASCADE)
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    booking_class = models.ForeignKey(BookingClass, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
