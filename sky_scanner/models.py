from django.db import models

# Create your models here.
from django.db import models

class DocumentType(models.Model):
    DOCUMENT_CHOICES = (
        ('PASSPORT', 'PASSPORT'),
        ('NATIONAL_ID', 'NATIONAL_ID'),
    )
    type = models.CharField(max_length=20, choices=DOCUMENT_CHOICES, unique=True)

class PassengerType(models.Model):
    PASSENGER_CHOICES = (
        ('ADULT', 'ADULT'),
        ('CHILD', 'CHILD'),
        ('INFANT', 'INFANT'),
    )
    type = models.CharField(max_length=10, choices=PASSENGER_CHOICES, unique=True)

class Gender(models.Model):
    GENDER_CHOICES = (
        ('M', 'M'),
        ('F', 'F'),
    )
    type = models.CharField(max_length=1, choices=GENDER_CHOICES, unique=True)

class Salutation(models.Model):
    SALUTATION_CHOICES = (
        ('MR', 'MR'),
        ('MS', 'MS'),
        ('MRS', 'MRS'),
        ('CHD', 'CHD'),
        ('INF', 'INF'),
    )
    type = models.CharField(max_length=5, choices=SALUTATION_CHOICES, unique=True)

class TicketStatus(models.Model):
    TICKET_STATUS_CHOICES = (
        ('ACTIVE', 'ACTIVE'),
        ('CANCELED', 'CANCELED'),
        ('REFUNDED', 'REFUNDED'),
    )
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, unique=True)

class BookingClass(models.Model):
    CLASS_CHOICES = (
        ('ECONOMY', 'ECONOMY'),
        ('PREMIUM_ECONOMY', 'PREMIUM_ECONOMY'),
        ('BUSINESS', 'BUSINESS'),
        ('FIRST', 'FIRST'),
    )
    type = models.CharField(max_length=20, choices=CLASS_CHOICES, unique=True)

class TicketNumber(models.Model):
    number = models.CharField(max_length=12, unique=True)

class BookingReference(models.Model):
    reference = models.CharField(max_length=6, unique=True)

class IATACode(models.Model):
    code = models.CharField(max_length=3, unique=True)

class AirlineCode(models.Model):
    code = models.CharField(max_length=2, unique=True)

class FlightNumber(models.Model):
    number = models.CharField(max_length=6, unique=True)
