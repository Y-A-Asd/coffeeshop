from django.test import TestCase
from .models import Food, Category
from django.test import Client
from django.urls import reverse
from .forms import CategoryCreateForm


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Main Category', parent=None)

    def test_category_str(self):
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), 'Main Category')

    def test_is_subcategory_false(self):
        category = Category.objects.get(id=1)
        self.assertFalse(category.is_subcategory)

    def test_is_subcategory_true(self):
        parent_category = Category.objects.get(id=1)
        sub_category = Category.objects.create(name='Sub Category', parent=parent_category)
        self.assertTrue(sub_category.is_subcategory)


class FoodModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Main Category', parent=None)
        Food.objects.create(name='Pizza', price=9.99, off=10, category=category)

    def test_food_str(self):
        food = Food.objects.get(id=1)
        self.assertEqual(str(food), 'Pizza')

    def test_price_after_off(self):
        food = Food.objects.get(id=1)
        expected_price = 8.99  # 10% off from 9.99
        self.assertEqual(food.price_after_off, expected_price)


class ListFoodViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/foods/list-food')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('foods:list-food'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Food_ListTemplate.html')


class CategoryCreateFormTest(TestCase):

    def test_category_form_valid(self):
        form_data = {'name': 'New Category'}
        form = CategoryCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_category_form_invalid(self):
        form_data = {'name': ''}  # empty name should be invalid
        form = CategoryCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
