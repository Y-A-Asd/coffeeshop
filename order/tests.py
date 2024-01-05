from django.test import TestCase, Client
from order.models import Order
from tables.models import Table
from order.forms import CartAddProductForm, OrderCreateForm
from foodmenu.models import Food
from django.urls import reverse


class OrderModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, status='E')
        Order.objects.create(customer_phone='09123456789', table=cls.table)

    def test_order_str(self):
        order = Order.objects.get(customer_phone='09123456789')
        expected_string = f"Order #{order.id} - 09123456789 - {order.table}"
        self.assertEqual(str(order), expected_string)


class CartAddProductFormTest(TestCase):

    def test_form_validity(self):
        form_data = {'quantity': 2, 'override': False}
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())


class OrderCreateFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, status='E')

    def test_order_create_form_valid(self):
        form_data = {'customer_phone': '09123456789', 'table': self.table.id}
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class CreateCartViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Food.objects.create(...)

    def test_create_cart_view_post(self):
        response = self.client.post(reverse('order:create-cart', args=[self.product.id]),
                                    {'quantity': 2, 'override': False})
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after adding to cart
        self.assertRedirects(response, reverse('order:detail-cart'))
