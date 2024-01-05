from django.test import TestCase
from tag.forms import TagCreateForm
from tag.models import Tag, TaggedItem
from foodmenu.models import Food, Category


class TagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(label='Test Tag', available=True)

    def test_str_method(self):
        tag = Tag.objects.get(label='Test Tag')
        self.assertEqual(str(tag), 'Test Tag')

    def test_default_availability(self):
        tag = Tag.objects.get(label='Test Tag')
        self.assertTrue(tag.available)
class TagCreateFormTest(TestCase):

    def test_tag_form_valid(self):
        form_data = {'label': 'New Tag', 'available': True}
        form = TagCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_tag_form_invalid(self):
        form_data = {'label': '', 'available': True}  # Empty label
        form = TagCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

class TaggedItemSignalTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Main Category')
        cls.tag_unavailable = Tag.objects.create(label='Unavailable', available=False)
        cls.tag_available = Tag.objects.create(label='Available', available=True)
        cls.food = Food.objects.create(name='Pizza', price=9.99, off=10, category=cls.category, availability=True)

    # def test_handle_taggeditem_generated(self):
    #     TaggedItem.objects.create(tag=self.tag_unavailable, content_object=self.food)
    #     self.food.refresh_from_db()
    #     self.assertFalse(self.food.availability)
    #     tagged_item = TaggedItem.objects.get(tag=self.tag_unavailable, content_object=self.food)
    #     tagged_item.tag = self.tag_available
    #     tagged_item.save()
    #     self.food.refresh_from_db()
    #     self.assertTrue(self.food.availability)

    # def test_handle_taggeditem_deletion(self):
    #     tagged_item = TaggedItem.objects.create(tag=self.tag_unavailable, content_object=self.food)
    #     tagged_item.delete()
    #     self.food.refresh_from_db()
    #     self.assertTrue(self.food.availability)
