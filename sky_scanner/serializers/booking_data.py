from rest_framework import serializers
from ..models import UserProfile, Traveller, Document, Ticket, Booking,Address,DocumentType
from django.contrib.auth import get_user_model
User = get_user_model()




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
    class Meta:
        model = Ticket
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Booking
        fields = '__all__'

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
