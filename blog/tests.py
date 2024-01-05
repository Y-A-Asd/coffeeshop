from django.test import TestCase, Client
from blog.forms import GenerateBlogForm
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User


class GenerateBlogFormTest(TestCase):

    def test_form_validity(self):
        form_data = {
            'title': 'Test Blog',
            'thumbnail': SimpleUploadedFile("bg_1.jpg", b"file_content", content_type="image/jpeg"),
            'content': 'This is a test blog content.'
        }
        form = GenerateBlogForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalidity(self):
        form_data = {
            'title': '',  # Empty title
            'content': 'This is a test blog content.'
        }
        form = GenerateBlogForm(data=form_data)
        self.assertFalse(form.is_valid())


class ListBlogViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_list_blog_view(self):
        response = self.client.get(reverse('blog:list-blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog_ListTemplate.html')


class CreateBlogViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_create_blog_view(self):
        response = self.client.get(reverse('blog:create-blog'))
        self.assertEqual(response.status_code, 302)


class CreateBlogSuperViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Create a superuser
        self.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        # Log in the superuser
        self.client.force_login(self.superuser)

    def test_get_create_blog_view(self):
        response = self.client.get(reverse('blog:create-blog'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog_CreateTemplate.html')