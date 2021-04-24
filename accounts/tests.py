from django.test import TestCase, Client
from django.urls import reverse, resolve
from . import views

# Create your tests here.

class TestURLs(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_home_page_url(self):
        url = reverse('home')
        response = resolve(url)
        
        self.assertEqual(response.func, views.home)

    def test_register_url(self):
        url = reverse('register')
        response = resolve(url)
        
        self.assertEqual(response.func, views.register)

    def test_login_url(self):
        url = reverse('login')
        response = resolve(url)
        
        self.assertEqual(response.func, views.login)

    def test_logout_url(self):
        url = reverse('logout')
        response = resolve(url)
        
        self.assertEqual(response.func, views.logout)