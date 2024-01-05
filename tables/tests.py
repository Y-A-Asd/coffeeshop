from tables.models import Table, Reservation as ReservationModel
from django.utils import timezone
from datetime import timedelta
from tables.forms import Reservation as ReservationForm
from django.urls import reverse
from django.test import TestCase, Client
from django.db.models.signals import post_migrate
from django.apps import apps


class ReservationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, status='E')
        ReservationModel.objects.create(
            phone_number='09123456789',
            datetime=timezone.now() + timedelta(days=2),
            number_of_persons=4,
            table=cls.table
        )

    def test_reservation_str(self):
        reservation = ReservationModel.objects.get(phone_number='09123456789')
        self.assertTrue(str(reservation).startswith('09123456789'))


class TableModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Table.objects.create(number=1, status='E')

    def test_table_str(self):
        table = Table.objects.get(id=1)
        self.assertEqual(str(table), '1')


class ReservationFormTest(TestCase):

    def test_reservation_form_valid(self):
        form_data = {
            'phone_number': '09123456789',
            'datetime': timezone.now() + timedelta(days=2),
            'number_of_persons': 4
        }
        form = ReservationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_reservation_form_invalid_phone_number(self):
        form_data = {
            'phone_number': 'invalid_phone_number',
            'datetime': timezone.now() + timedelta(days=2),
            'number_of_persons': 4
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_reservation_form_invalid_datetime(self):
        form_data = {
            'phone_number': '09123456789',
            'datetime': timezone.now() - timedelta(days=1),  # Past date
            'number_of_persons': 4
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('datetime', form.errors)

    def test_reservation_form_invalid_number_of_persons(self):
        form_data = {
            'phone_number': '09123456789',
            'datetime': timezone.now() + timedelta(days=2),
            'number_of_persons': 0  # Invalid number of persons
        }
        form = ReservationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('number_of_persons', form.errors)


class CreateReservationViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_create_reservation_view(self):
        response = self.client.get(reverse('tables:create-reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Reservation_CreateTemplate.html')


class ListReservationViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_list_reservation_view(self):
        response = self.client.get(reverse('tables:list-reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Reservation_ListTemplate.html')


class PostMigrateSignalTest(TestCase):

    def test_create_default_table(self):
        # Trigger post_migrate signal
        post_migrate.send(sender=apps.get_app_config('tables'))

        # Check if the default table with status 'T' is created
        self.assertTrue(Table.objects.filter(status='T').exists())
