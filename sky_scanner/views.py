from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime,timedelta
from rest_framework.decorators import action

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
    
    @action(detail=False, methods=['GET'])
    def user_bookings(self, request):
        user_bookings = Booking.objects.filter(user=request.user) # Assuming you have a timestamp called `created_at` in your Booking model
        serializer = BookingSerializer(user_bookings, many=True)
        return Response(serializer.data)

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
        origin__city=departure_location,
        destination__city=arrival_location,
        departure_date=departure_date
    )
    # You can extend this with more conditions if needed
    # For example: Filter by available seats, flight status, etc.
    return flights.first() if flights else None


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        data = request.data.copy()  # Making a mutable copy of the request data
        user = request.user
        # Check if UserProfile exists, if not, create one
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Extracting necessary details
        traveller_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'frequent_flyer_number': user.frequent_flyer_number,
            'document': user_profile.document.id if user_profile.document else None,
            'linked_user_account': user.id,
        }

        # Get or create traveller
        traveller, created = Traveller.objects.get_or_create(
            linked_user_account=user.id, 
            defaults=traveller_data,
            email=user.email
        )

        if not created and any([getattr(traveller, key) != value for key, value in traveller_data.items()]):
            # Update the traveller if any information has changed
            for key, value in traveller_data.items():
                setattr(traveller, key, value)
            traveller.save()

        departure_location = data.pop('departure_location')
        arrival_location = data.pop('arrival_location')

        departure_date_string = data.pop('departure_date')
        departure_date = datetime.strptime(departure_date_string, "%Y-%m-%d").date()

        # Find a suitable flight
        flight = find_flight(departure_location, arrival_location, departure_date)
        
        if not flight:
            return Response({"error": "No available flight found for the given criteria."}, status=status.HTTP_400_BAD_REQUEST)
                    # Generate a random ticket number
        random_ticket_number = random.randint(100000, 999999)  # assuming 6 digit ticket numbers
        random_airline_code = ''.join(random.choices(string.ascii_uppercase, k=3))

        ticket_number = TicketNumber.objects.create(number=random_ticket_number)
        ticketing_airline=AirlineCode.objects.create(code=random_airline_code)
        print(ticket_number.id)
        print(ticketing_airline.id)

        ticket_data = {
            'ticket_number': ticket_number,
            'ticketing_airline': ticketing_airline,
            'issued_date': datetime.now().date(),
            'traveller': traveller,
        }

        ticket = Ticket.objects.create(**ticket_data)
        
        # Adding the found flight to your booking data
        data['flight'] = flight.id
        data['user'] = user.id
        data['tickets'] = [ticket.id]

        from decimal import Decimal
    
                # Assuming you have the necessary information in your request.data
        booking_class, created = BookingClass.objects.get_or_create(type="ECONOMY")
        booked_segment_data = {
            'origin': IATACode.objects.get(city=departure_location),
            'destination': IATACode.objects.get(city=arrival_location),
            # 'flight_number': FlightNumber.objects.get(number=data['flight_number']),
            'flight_Date': departure_date,
            'airline_code': ticketing_airline,  # Assuming the airline for the booked segment is the same as the ticketing airline
            'departure_date': departure_date,
            'price': Decimal(flight.price),
            'booking_class':booking_class
        }

        booked_segment = BookedSegment.objects.create(**booked_segment_data)
        ticket.booked_segments.add(booked_segment)
        booking_serializer = BookingCreateSerializer(data=data)


        if booking_serializer.is_valid():
            booking_serializer.save()
            return Response(booking_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

from rest_framework.decorators import action
from .rewards import RewardSystem

class DiscountInfoViewSet(viewsets.ViewSet):
    
    @action(detail=False, methods=['GET'])
    def discount_info(self, request):
        user = request.user.id
        reward_system = RewardSystem(user)
        discount_info = reward_system.get_discount_info()

        return Response(discount_info)