from rest_framework import serializers
from ..models import UserProfile, Traveller, PromoCode, Document, Ticket, Booking,Address,DocumentType,BookedSegment
from django.contrib.auth import get_user_model
from .flight_data import BookedSegmentSerializer,ShowBookedSegmentSerializer
from custom_auth.models import Referral,ReferralCode
User = get_user_model()

class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ('user', 'code', 'validity', 'points_consumed')

class RewardInfoSerializer(serializers.Serializer):
    total_points = serializers.IntegerField()
    discount_percentage = serializers.FloatField()
    max_points = serializers.IntegerField(default=500)  # This is from your POINTS_FOR_MAX_DISCOUNT constant

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ['user', 'code']

class ReferralSerializer(serializers.ModelSerializer):
    referrer_email = serializers.ReadOnlyField(source='referrer.email')
    referred_email = serializers.ReadOnlyField(source='referred.email')

    class Meta:
        model = Referral
        fields = ['referrer', 'referrer_email', 'referred', 'referred_email', 'date_referred']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class TravellerSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()
    first_name = serializers.CharField(source='first_name')  # Add this
    middle_name = serializers.CharField(source='middle_name')  # And this

    class Meta:
        model = Traveller
        fields = '__all__'

    def create(self, validated_data):
        document_data = validated_data.pop('document')
        document = Document.objects.create(**document_data)
        traveller = Traveller.objects.create(document=document, **validated_data)
        return traveller

    def update(self, instance, validated_data):
        document_data = validated_data.pop('document')
        document = instance.document

        for attr, value in document_data.items():
            setattr(document, attr, value)
        document.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class TicketSerializer(serializers.ModelSerializer):
    booked_segments = serializers.PrimaryKeyRelatedField(many=True, queryset=BookedSegment.objects.all())
    
    class Meta:
        model = Ticket
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert the booked_segments from ID to serialized data only for GET requests
        data['booked_segments'] = ShowBookedSegmentSerializer(instance.booked_segments.all(), many=True).data
        return data
    

class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)
    
    class Meta:
        model = Booking
        fields = '__all__'

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
    
    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        booking = Booking.objects.create(**validated_data)

        for ticket in tickets_data:
            booking.tickets.add(ticket)
        
        return booking


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'frequent_flyer_number', 'date_of_birth']

class AddressEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'postal_code']

class DocumentTypeEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['type']

class UserProfileEditSerializer(serializers.ModelSerializer):
    address = AddressEditSerializer()
    document = DocumentTypeEditSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'address', 'document']
