from django.test import TestCase
from foodmenu.models import Category, Food
from utils import json_menu_generator,is_parent,Reporting
from order.models import Order, OrderItem
from tables.models import Table

class JsonMenuGeneratorTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        parent_category = Category.objects.create(name="Parent Category")
        sub_category = Category.objects.create(name="Sub Category", parent=parent_category)
        Food.objects.create(name="Food 1", price=10, category=parent_category)
        Food.objects.create(name="Food 2", price=20, category=sub_category)

    def test_json_menu_generator(self):
        menu = json_menu_generator()
        self.assertIsInstance(menu, list)
        self.assertEqual(len(menu), 1)
        self.assertIn('subcategories', menu[0])
        self.assertEqual(len(menu[0]['subcategories']), 1)
        self.assertEqual(menu[0]['subcategories'][0]['name'], "Sub Category")
class IsParentTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.parent_category = Category.objects.create(name="Parent Category")
        cls.sub_category = Category.objects.create(name="Sub Category", parent=cls.parent_category)

    def test_is_parent_with_parent_category(self):
        self.assertTrue(is_parent(self.parent_category))

    def test_is_parent_with_sub_category(self):
        self.assertFalse(is_parent(self.sub_category))
class ReportingTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        food = Food.objects.create(name="Test Food", price=100)
        table = Table.objects.create(number=1)
        order = Order.objects.create(table=table, status='F')
        OrderItem.objects.create(order=order, product=food, price=food.price, quantity=2)

    def test_total_sales(self):
        reporting = Reporting({'days': 30})
        result = reporting.total_sales()
        self.assertEqual(result, 200)  # 2 items at 100 each