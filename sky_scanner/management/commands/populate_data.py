# sky_scanner/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from sky_scanner.models import *
from faker import Faker
import random
from django.contrib.auth import get_user_model
User = get_user_model()

# Current date
current_date = datetime.now()
# Check if the date is before or in October 2023
if current_date < datetime(2023, 10, 1):
    start_date = datetime(2023, 10, 1)
else:
    start_date = current_date
end_date = datetime(2023, 12, 31)

real_airports = [
    {"code": "FCO", "airport_name": "Leonardo da Vinci–Fiumicino Airport", "city": "Rome"},
    {"code": "TIA", "airport_name": "Tirana International Airport Nënë Tereza", "city": "Tirana"},
    {"code": "LHR", "airport_name": "Heathrow Airport", "city": "London"},
    {"code": "JFK", "airport_name": "John F. Kennedy International Airport", "city": "New York City"},
    # Adding more airports
    {"code": "DXB", "airport_name": "Dubai International Airport", "city": "Dubai"},
    {"code": "NRT", "airport_name": "Narita International Airport", "city": "Tokyo"},
    {"code": "SYD", "airport_name": "Sydney Kingsford Smith Airport", "city": "Sydney"},
]


class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for airport in real_airports:
            IATACode.objects.get_or_create(
        code=airport["code"],
        airport_name=airport["airport_name"],
        city=airport["city"]
    )
            
        for _ in range(5):
            AirlineCode.objects.get_or_create(code=fake.unique.lexify(text="??", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            FlightNumber.objects.get_or_create(number=fake.unique.lexify(text="??????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            DocumentType.objects.get_or_create(type=random.choice(['PASSPORT', 'NATIONAL_ID']))
            PassengerType.objects.get_or_create(type=random.choice(['ADULT', 'CHILD', 'INFANT']))
            Gender.objects.get_or_create(type=random.choice(['M', 'F']))
            Salutation.objects.get_or_create(type=random.choice(['MR', 'MS', 'MRS', 'CHD', 'INF']))
            TicketStatus.objects.get_or_create(status=random.choice(['ACTIVE', 'CANCELED', 'REFUNDED']))
            BookingClass.objects.get_or_create(type=random.choice(['ECONOMY', 'PREMIUM_ECONOMY', 'BUSINESS', 'FIRST']))
            TicketNumber.objects.get_or_create(number=fake.unique.numerify(text="############"))
            BookingReference.objects.get_or_create(reference=fake.unique.lexify(text="??????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

        for _ in range(5):
            address = Address.objects.create(
                street=fake.street_name(),
                city=fake.city(),
                postal_code=fake.zipcode()
            )
            contact = Contact.objects.create(
                email=fake.email(),
                phone=fake.phone_number(),
                address=address
            )
            origin = IATACode.objects.order_by('?').first()
            destination = IATACode.objects.exclude(id=origin.id).order_by('?').first()

            document = Document.objects.create(
                document_type=DocumentType.objects.order_by('?').first(),
                document_number=fake.unique.numerify(text="########"),
                personal_number=fake.unique.numerify(text="########"),
                issuing_country=fake.country_code(),
                issued_date=fake.date(),
                expiry_date=fake.date()
            )

            traveller = Traveller.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.first_name(),
                salutation=Salutation.objects.order_by('?').first(),
                gender=Gender.objects.order_by('?').first(),
                passenger_type=PassengerType.objects.order_by('?').first(),
                document=document,
                contact=contact
            )

            # Generate a random ticket number
            random_ticket_number = random.randint(100000, 999999)  # assuming 6 digit ticket numbers

            # Generate a random airline code (e.g., 3 uppercase letters)
            random_airline_code = ''.join(random.choices(string.ascii_uppercase, k=3))
            created,ticket_number = TicketNumber.objects.create(number=random_ticket_number),
            created,ticketing_airline=AirlineCode.objects.create(code=random_airline_code),
            ticket_status =TicketStatus.objects.create(status="ACTIVE").id
            print(ticket_number)
            print(ticketing_airline)

            ticket = Ticket.objects.create(
                ticket_number= ticket_number.id,
                ticketing_airline=ticketing_airline.id,
                issued_date=fake.date(),
                traveller=traveller
            )

            origin = IATACode.objects.order_by('?').first()
            destination = IATACode.objects.exclude(id=origin.id).order_by('?').first()

            booked_segment = BookedSegment.objects.create(
                origin=origin,
                destination=destination,
                flight_number=FlightNumber.objects.order_by('?').first(),
                flight_Date=fake.date(),
                airline_code=AirlineCode.objects.order_by('?').first(),
                departure_date=fake.date_time(),
                booking_class=BookingClass.objects.order_by('?').first(),
                price = round(fake.random.uniform(10, 500), 2),
                tax_percentage = round(fake.random.uniform(1, 100), 2)
            )
            ticket.booked_segments.add(booked_segment)
                
        
        # Iterate over each airport
        for origin in IATACode.objects.all():
            for _ in range(50):  # Generate 50 flights for each origin
                destination = IATACode.objects.exclude(id=origin.id).order_by('?').first()
                
# Randomly generate departure date within the given range
                departure_date = fake.date_between_dates(start_date, end_date)  # Change here: generate only date

                # Generate a random price for the flight, e.g., between 50 to 500
                flight_price = round(fake.random.uniform(50, 500), 2)

                # Calculate the arrival date based on the departure date and flight duration

                flight_number = fake.unique.lexify(text="??????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")

                Flight.objects.create(
                    flight_number=flight_number,
                    origin=origin,
                    destination=destination,
                    departure_date=departure_date,
                    price=flight_price  # Add the generated price here
                )



        date_of_birth = fake.date_between(start_date="-100y", end_date="-18y")  # This ensures the generated user is between 18 and 100 years old.

        user = User.objects.create(email=fake.email(),date_of_birth=date_of_birth)

        booking = Booking.objects.create(
            booking_reference=BookingReference.objects.order_by('?').first(),
            user=user
        )
        booking.tickets.add(ticket)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
