# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (FlightViewSet, DocumentTypeViewSet, PassengerTypeViewSet, GenderViewSet, 
                    SalutationViewSet, TicketStatusViewSet, BookingClassViewSet, 
                    TicketNumberViewSet, BookingReferenceViewSet, IATACodeViewSet, 
                    AirlineCodeViewSet, FlightNumberViewSet, AddressViewSet, 
                    ContactViewSet, BookedSegmentViewSet)
from sky_scanner.views import CityListViewSet

router = DefaultRouter()
router.register(r'flights', FlightViewSet)
router.register(r'document-types', DocumentTypeViewSet)
router.register(r'passenger-types', PassengerTypeViewSet)
router.register(r'genders', GenderViewSet)
router.register(r'salutations', SalutationViewSet)
router.register(r'ticket-statuses', TicketStatusViewSet)
router.register(r'booking-classes', BookingClassViewSet)
router.register(r'ticket-numbers', TicketNumberViewSet)
router.register(r'booking-references', BookingReferenceViewSet)
router.register(r'iata-codes', IATACodeViewSet)
router.register(r'airline-codes', AirlineCodeViewSet)
router.register(r'flight-numbers', FlightNumberViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'booked-segments', BookedSegmentViewSet)
router.register(r'cities', CityListViewSet, basename='city')

urlpatterns = [
    path('', include(router.urls)),
]

print(urlpatterns)