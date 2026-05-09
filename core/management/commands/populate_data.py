from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from services.models import ServiceCategory, Service
from shop.models import ProductCategory, Product
from bookings.models import Artist, TimeSlot
from datetime import time

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating data...')

        # Service Categories
        bridal_cat, _ = ServiceCategory.objects.get_or_create(
            name='Bridal Mehandi',
            description='Intricate and heavy designs for the bride.'
        )
        party_cat, _ = ServiceCategory.objects.get_or_create(
            name='Party Mehandi',
            description='Elegant and light designs for guests.'
        )
        arabic_cat, _ = ServiceCategory.objects.get_or_create(
            name='Arabic Designs',
            description='Beautiful floral and geometric patterns.'
        )

        # Services
        Service.objects.get_or_create(
            name='Royal Bridal Mehandi',
            category=bridal_cat,
            description='Full hands and feet traditional bridal design.',
            short_description='Full hands and feet traditional bridal design.',
            duration='4-6 hours',
            price=15000,
            discount_price=12000,
            is_featured=True
        )
        Service.objects.get_or_create(
            name='Minimalist Party Mehandi',
            category=party_cat,
            description='Simple and elegant design for one hand.',
            short_description='Simple and elegant design for one hand.',
            duration='30-45 mins',
            price=500,
            is_featured=True
        )
        Service.objects.get_or_create(
            name='Classic Arabic Mehandi',
            category=arabic_cat,
            description='Traditional Arabic design flowing from finger to wrist.',
            short_description='Traditional Arabic design flowing from finger to wrist.',
            duration='1-2 hours',
            price=1500,
            is_featured=True
        )

        # Product Categories
        cone_cat, _ = ProductCategory.objects.get_or_create(name='Henna Cones')
        powder_cat, _ = ProductCategory.objects.get_or_create(name='Henna Powder')
        oil_cat, _ = ProductCategory.objects.get_or_create(name='Essential Oils')

        # Products
        Product.objects.get_or_create(
            name='Organic Bridal Henna Cone (Pack of 12)',
            category=cone_cat,
            description='100% natural, chemical-free henna cones for rich stain.',
            short_description='100% natural, chemical-free henna cones.',
            price=350,
            stock=50,
            is_featured=True
        )
        Product.objects.get_or_create(
            name='Premium Rajasthani Henna Powder (500g)',
            category=powder_cat,
            description='Triple-sifted, fine quality henna powder from Sojat.',
            short_description='Triple-sifted, fine quality henna powder.',
            price=450,
            discount_price=400,
            stock=30,
            is_featured=True
        )
        Product.objects.get_or_create(
            name='Mehandi Oil Mix (50ml)',
            category=oil_cat,
            description='Blend of essential oils for darker and long-lasting stain.',
            short_description='Blend of essential oils for darker stain.',
            price=250,
            stock=100,
            is_featured=True
        )

        # Artists
        Artist.objects.get_or_create(
            name='Aisha Khan',
            bio='Expert in traditional bridal and portrait mehandi.',
            specialization='Bridal Mehandi',
            experience_years=10
        )
        Artist.objects.get_or_create(
            name='Neha Sharma',
            bio='Creative artist specializing in modern and Arabic designs.',
            specialization='Arabic & Modern',
            experience_years=5
        )

        # Time Slots
        TimeSlot.objects.get_or_create(label='Morning (09:00 AM - 12:00 PM)', start_time=time(9, 0), end_time=time(12, 0))
        TimeSlot.objects.get_or_create(label='Afternoon (12:00 PM - 03:00 PM)', start_time=time(12, 0), end_time=time(15, 0))
        TimeSlot.objects.get_or_create(label='Evening (03:00 PM - 06:00 PM)', start_time=time(15, 0), end_time=time(18, 0))

        # Admin user
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Created superuser: admin / admin')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data.'))
