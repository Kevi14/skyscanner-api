from django.db import models
from .flight_data import *
from .reference_data import * 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()


import random
import string

def generate_referral_code():
    """Generate a random 8-character referral code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="referral_code")
    code = models.CharField(max_length=8, unique=True, default=generate_referral_code)
    
    def __str__(self):
        return self.code

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referrals_made")
    referred = models.ForeignKey(User, on_delete=models.CASCADE, related_name="referred_by")
    date_referred = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['referrer', 'referred']  # Ensure that a user can't refer the same person multiple times

    def __str__(self):
        return f"{self.referrer.email} -> {self.referred.email}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    address = models.ForeignKey('sky_scanner.Address', on_delete=models.SET_NULL, null=True)
    document = models.ForeignKey('sky_scanner.DocumentType', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.email
    

class Traveller(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    salutation = models.ForeignKey(Salutation, on_delete=models.CASCADE,blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,blank=True, null=True)
    passenger_type = models.ForeignKey(PassengerType, on_delete=models.CASCADE,blank=True, null=True)
    document = models.ForeignKey('Document', on_delete=models.CASCADE,blank=True, null=True)
    frequent_flyer_number = models.CharField(max_length=255, blank=True, null=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE,blank=True, null=True)
    linked_user_account = models.CharField(max_length=255, blank=True, null=True)
    email =models.EmailField()

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
    # ticket_status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE)
    issued_date = models.DateField()
    traveller = models.ForeignKey(Traveller, on_delete=models.CASCADE)
    booked_segments = models.ManyToManyField(BookedSegment)

class Booking(models.Model):
    # booking_reference = models.ForeignKey(BookingReference, on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model defined