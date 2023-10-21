from django.db import models
from .flight_data import *
from .reference_data import * 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.ForeignKey('sky_scanner.Address', on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey('sky_scanner.DocumentType', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.email
    

class Traveller(models.Model):
    first_mame = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_mame = models.CharField(max_length=255, blank=True, null=True)
    salutation = models.ForeignKey(Salutation, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    passenger_type = models.ForeignKey(PassengerType, on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    frequent_flyer_number = models.CharField(max_length=255, blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    linked_user_account = models.CharField(max_length=255, blank=True, null=True)

class Document(models.Model):
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    document_number = models.CharField(max_length=255)
    personal_number = models.CharField(max_length=255)
    issuing_country = models.CharField(max_length=50)
    issued_date = models.DateField()
    expiry_date = models.DateField()  

    
class Ticket(models.Model):
    ticket_number = models.ForeignKey(TicketNumber, on_delete=models.CASCADE)
    ticketing_airline = models.ForeignKey(AirlineCode, on_delete=models.CASCADE)
    ticket_status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE)
    issued_date = models.DateField()
    traveller = models.ForeignKey(Traveller, on_delete=models.CASCADE)
    booked_segments = models.ManyToManyField(BookedSegment)

class Booking(models.Model):
    booking_reference = models.ForeignKey(BookingReference, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model defined