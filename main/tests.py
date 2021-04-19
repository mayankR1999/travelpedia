from django.test import TestCase, Client

# Create your tests here.

class TestURLs(TestCase):
    def setUp(self):
        self.client = Client()

    def test_feed_page_response(self):
        response = self.client.get('/user/')
        
        self.assertEqual(response.status_code, 200)

    def test_upload_page_response(self):
        response = self.client.get('/user/upload')
        
        self.assertEqual(response.status_code, 200)
        