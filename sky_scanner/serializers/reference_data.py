from rest_framework import serializers

from ..models import (DocumentType, PassengerType, Gender, Salutation, TicketStatus, 
                     BookingClass, TicketNumber, BookingReference, IATACode, 
                     AirlineCode, FlightNumber)

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

class PassengerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerType
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class SalutationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salutation
        fields = '__all__'

class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = '__all__'

class BookingClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingClass
        fields = '__all__'

class TicketNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketNumber
        fields = '__all__'

class BookingReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingReference
        fields = '__all__'

class IATACodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IATACode
        fields = '__all__'

class AirlineCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirlineCode
        fields = '__all__'

class FlightNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightNumber
        fields = '__all__'

class CitySerializer(serializers.ListSerializer):
    child = serializers.CharField()
