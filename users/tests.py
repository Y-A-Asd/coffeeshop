from django.test import TestCase,Client
from users.models import User
from users.backend import PhoneBackend
from users.forms import LoginForm, RegistrationForm
from django.urls import reverse

class PhoneBackendTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(phone_number='09123456789', email='test@example.com', password='testpassword123')

    def test_authenticate_valid_user(self):
        backend = PhoneBackend()
        user = backend.authenticate(None, phone_number='09123456789', password='testpassword123')
        self.assertIsNotNone(user)
        self.assertEqual(user.phone_number, '09123456789')

    def test_authenticate_invalid_user(self):
        backend = PhoneBackend()
        user = backend.authenticate(None, phone_number='09999999999', password='wrongpassword')
        self.assertIsNone(user)
class LoginFormTest(TestCase):

    def test_login_form_valid(self):
        form_data = {'phone_number': '09123456789', 'password': 'mypassword'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid(self):
        form_data = {'phone_number': 'invalid', 'password': 'mypassword'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

class RegistrationFormTest(TestCase):

    def test_registration_form_valid(self):
        form_data = {'phone_number': '09123456789', 'email': 'test@example.com', 'verification_method': 'email'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        form_data = {'phone_number': 'invalid', 'email': 'test@example.com', 'verification_method': 'email'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
class UsersLoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(phone_number='09123456789', email='test@example.com', password='testpassword123')

    def test_get_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_post_login_view_valid_credentials(self):
        response = self.client.post(reverse('users:login'), {'phone_number': '09123456789', 'password': 'testpassword123'})
        self.assertEqual(response.status_code, 302)  # Assuming successful login redirects

    def test_post_login_view_invalid_credentials(self):
        response = self.client.post(reverse('users:login'), {'phone_number': '09123456789', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # Assuming stay on page with error message
