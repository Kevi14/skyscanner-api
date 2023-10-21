from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from rest_framework import viewsets,status
from .models import *
from .serializers import *
from .models import Address, Contact, BookedSegment
from .serializers import AddressSerializer, ContactSerializer, BookedSegmentSerializer
import django_filters

# Reference Data
class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer

class PassengerTypeViewSet(viewsets.ModelViewSet):
    queryset = PassengerType.objects.all()
    serializer_class = PassengerTypeSerializer

class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

class SalutationViewSet(viewsets.ModelViewSet):
    queryset = Salutation.objects.all()
    serializer_class = SalutationSerializer

class TicketStatusViewSet(viewsets.ModelViewSet):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer

class BookingClassViewSet(viewsets.ModelViewSet):
    queryset = BookingClass.objects.all()
    serializer_class = BookingClassSerializer

class TicketNumberViewSet(viewsets.ModelViewSet):
    queryset = TicketNumber.objects.all()
    serializer_class = TicketNumberSerializer

class BookingReferenceViewSet(viewsets.ModelViewSet):
    queryset = BookingReference.objects.all()
    serializer_class = BookingReferenceSerializer

class IATACodeViewSet(viewsets.ModelViewSet):
    queryset = IATACode.objects.all()
    serializer_class = IATACodeSerializer

class AirlineCodeViewSet(viewsets.ModelViewSet):
    queryset = AirlineCode.objects.all()
    serializer_class = AirlineCodeSerializer

class FlightNumberViewSet(viewsets.ModelViewSet):
    queryset = FlightNumber.objects.all()
    serializer_class = FlightNumberSerializer

# Flight data


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        address_data = self.request.data.get('address')
        address = Address.objects.create(**address_data)
        serializer.save(address=address)

    def perform_update(self, serializer):
        address_data = self.request.data.get('address')
        address = self.get_object().address

        for attr, value in address_data.items():
            setattr(address, attr, value)
        address.save()

        serializer.save()

class BookedSegmentViewSet(viewsets.ModelViewSet):
    queryset = BookedSegment.objects.all()
    serializer_class = BookedSegmentSerializer

# booking data 

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        address_data = self.request.data.get('address')
        address = Address.objects.create(**address_data)
        serializer.save(address=address)

    def perform_update(self, serializer):
        address_data = self.request.data.get('address')
        address = self.get_object().address

        for attr, value in address_data.items():
            setattr(address, attr, value)
        address.save()

        serializer.save()

class BookedSegmentViewSet(viewsets.ModelViewSet):
    queryset = BookedSegment.objects.all()
    serializer_class = BookedSegmentSerializer

# views.py
class FlightFilter(django_filters.FilterSet):
    origin_city = django_filters.CharFilter(field_name='origin__city', lookup_expr='icontains')
    destination_city = django_filters.CharFilter(field_name='destination__city', lookup_expr='icontains')

    class Meta:
        model = Flight
        fields = ['origin_city', 'destination_city']

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FlightFilter


class CityListViewSet(viewsets.ViewSet):
    
    def list(self, request):
        origin_cities = Flight.objects.values_list('origin__city', flat=True).distinct()
        destination_cities = Flight.objects.values_list('destination__city', flat=True).distinct()

        all_cities = set(origin_cities) | set(destination_cities)  # Combining and deduping the lists
        
        # Convert list of city names to a list of dictionaries
        city_data = [{city: city} for city in all_cities]

        serializer = CitySerializer(city_data, many=True)
        data = [x[0] for x in serializer.data]
        return Response(data)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        user_data = request.data.get('user')
        address_data = request.data.get('address')
        document_data = request.data.get('document')

        # Update User
        user_serializer = UserEditSerializer(profile.user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        # Update Address
        address_serializer = AddressEditSerializer(profile.address, data=address_data, partial=True)
        if address_serializer.is_valid():
            address_serializer.save()

        # Update DocumentType
        document_serializer = DocumentTypeEditSerializer(profile.document, data=document_data, partial=True)
        if document_serializer.is_valid():
            document_serializer.save()

        # Update UserProfile
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
def find_flight(departure_location, arrival_location, departure_date):
    # Assuming you have a Flight model
    flights = Flight.objects.filter(
        departure_location=departure_location,
        arrival_location=arrival_location,
        departure_date=departure_date,
    )

    # You can extend this with more conditions if needed
    # For example: Filter by available seats, flight status, etc.
    return flights.first() if flights else None
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user 
        departure_location = data.pop('departure_location')
        arrival_location = data.pop('arrival_location')
        departure_date = data.pop('departure_date')
        # Find a suitable flight
        flight = find_flight(departure_location, arrival_location, departure_date)
        
        if not flight:
            return Response({"error": "No available flight found for the given criteria."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Adding the found flight to your booking data
        data['flight'] = flight.id
        data['user'] = user.id

        tickets_data = data.pop('tickets', [])
        booking_serializer = BookingSerializer(data=data)

        if booking_serializer.is_valid():
            booking = booking_serializer.save()
            for ticket_data in tickets_data:
                traveller_data = ticket_data.pop('traveller')
                traveller_serializer = TravellerSerializer(data=traveller_data)
                
                if traveller_serializer.is_valid():
                    traveller = traveller_serializer.save()
                    ticket_data['traveller'] = traveller.id
                    ticket_serializer = TicketSerializer(data=ticket_data)

                    if ticket_serializer.is_valid():
                        ticket = ticket_serializer.save()
                        booking.tickets.add(ticket)
                    else:
                        booking.delete()  # Clean up booking if ticket creation fails
                        return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    booking.delete()  # Clean up booking if traveller creation fails
                    return Response(traveller_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(booking_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
