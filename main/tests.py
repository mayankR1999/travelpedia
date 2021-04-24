from django.test import TestCase, Client
from django.urls import reverse, resolve
from . import views

# Create your tests here.

class TestURLs(TestCase):
    def setUp(self):
        self.client = Client()

    def test_of_user_feed_url(self):
        url = reverse('user_feed')
        response = resolve(url)
        
        self.assertEqual(response.func, views.userFeed)

    def test_upload_page_url(self):
        url = reverse('post_upload')
        response = resolve(url)
        
        self.assertEqual(response.func, views.post_upload)

    def test_search_post_url(self):
        url = reverse('searchPost')
        response = resolve(url)
        
        self.assertEqual(response.func, views.searchPost)

    def test_like_post_url(self):
        url = reverse('like_post')
        response = resolve(url)
        
        self.assertEqual(response.func, views.likePost)
    
    def test_my_post_url(self):
        url = reverse('show_my_posts')
        response = resolve(url)
        
        self.assertEqual(response.func, views.show_my_posts)
    
    def test_delete_post_url(self):
        url = reverse('delete_post')
        response = resolve(url)
        
        self.assertEqual(response.func, views.delete_post)