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
    
    def test_user_profile_url(self):
        url = reverse('show_user_profile', args=[1])
        response = resolve(url)
        
        self.assertEqual(response.func, views.show_user_profile)

    def test_change_dp_url(self):
        url = reverse('change_dp')
        response = resolve(url)
        
        self.assertEqual(response.func, views.change_dp)

    def test_remove_dp_url(self):
        url = reverse('remove_dp')
        response = resolve(url)
        
        self.assertEqual(response.func, views.remove_dp)

    def test_change_bio_url(self):
        url = reverse('change_bio')
        response = resolve(url)
        
        self.assertEqual(response.func, views.change_bio)
    
    def test_delete_post_url(self):
        url = reverse('delete_post')
        response = resolve(url)
        
        self.assertEqual(response.func, views.delete_post)

    def test_follow_toggle_url(self):
        url = reverse('follow_toggle_request')
        response = resolve(url)

        self.assertEqual(response.func, views.follow_toggle)