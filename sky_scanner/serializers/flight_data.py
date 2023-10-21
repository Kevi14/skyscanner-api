from rest_framework import serializers
from ..models import Address, Contact, BookedSegment,Flight
from .reference_data import IATACodeSerializer


class BookedSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedSegment
        fields = '__all__'

class FlightSerializer(serializers.ModelSerializer):
    origin = IATACodeSerializer()  # Use the IATACode serializer for origin
    destination = IATACodeSerializer()  # Use the IATACode serializer for destination

    class Meta:
        model = Flight
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        contact = Contact.objects.create(address=address, **validated_data)
        return contact

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address

        for attr, value in address_data.items():
            setattr(address, attr, value)
        address.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
