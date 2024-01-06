from core.models import BaseModel
from django.test import TestCase, Client
from django.utils import timezone
from core.models import AuditLog
from django.contrib.auth import get_user_model
from django.urls import reverse
from users.models import User
from users.backends import PhoneBackend


# class BaseModelTest(TestCase):
#
#     def test_soft_delete(self):
#         instance = BaseModel()
#         instance.save()
#         self.assertIsNone(instance.deleted_at)
#         instance.delete()
#         self.assertIsNotNone(instance.deleted_at)
#         self.assertTrue(isinstance(instance.deleted_at, timezone.datetime))
#

class AuditLogTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(email='testuser@gms.com', phone_number= '09353220545',password='12345')
        AuditLog.objects.create(
            user=cls.user,
            action='CREATE',
            table_name='test_table',
            row_id='1',
            old_value={'field': 'value'}
        )

    def test_audit_log_creation(self):
        log = AuditLog.objects.get(user=self.user)
        self.assertEqual(log.action, 'CREATE')
        self.assertEqual(log.table_name, 'test_table')
        self.assertEqual(log.row_id, '1')
        self.assertEqual(log.old_value, {'field': 'value'})


class DashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(phone_number='09123456789', email='test@example.com',
                                             password='testpassword')
        backend = PhoneBackend()
        user = backend.authenticate(None, phone_number='09123456789', password='testpassword')
        self.client.force_login(user, backend='users.backend.PhoneBackend')

    def test_dashboard_view(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, 'Core_DashboardTemplate.html')
