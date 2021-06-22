from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
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


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create_user(username = 'test_user', email = 'test@travelpedia.com',
        password = 'testpass', first_name = 'test', last_name = 'user')

    def test_home_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_register_user_GET(self):
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_user_POST_adds_new_user(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'test2',
            'last_name': 'user2',
            'user_name': 'test_user2',
            'email': 'test2@travelpedia.com',
            'pass1': 'Test123#',
            'pass2': 'Test123#',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.filter(username = 'test_user2').exists(), True)

    def test_register_user_POST_short_username(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'test2',
            'last_name': 'user2',
            'user_name': 'tes',
            'email': 'test2@travelpedia.com',
            'pass1': 'Test123#',
            'pass2': 'Test123#',
        }, follow = True)

        messages = list(response.context.get('messages'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(messages), 1)
        self.assertEquals(messages[0].message, 'invalid username, must contain atleast 4 letters.')

    def test_register_user_POST_username_already_exists(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'test2',
            'last_name': 'user2',
            'user_name': 'test_user',
            'email': 'test2@travelpedia.com',
            'pass1': 'Test123#',
            'pass2': 'Test123#',
        }, follow = True)

        messages = list(response.context.get('messages'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(messages), 1)
        self.assertEquals(messages[0].message, 'username already exists.')

    def test_register_user_POST_email_already_associated(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'test2',
            'last_name': 'user2',
            'user_name': 'test_user2',
            'email': 'test@travelpedia.com',
            'pass1': 'Test123#',
            'pass2': 'Test123#',
        }, follow = True)

        messages = list(response.context.get('messages'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(messages), 1)
        self.assertEquals(messages[0].message, 'email already associated with an account.')

    def test_register_user_POST_passwords_do_not_match(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'test2',
            'last_name': 'user2',
            'user_name': 'test_user2',
            'email': 'test2@travelpedia.com',
            'pass1': 'Test123#',
            'pass2': 'Test1#',
        }, follow = True)

        messages = list(response.context.get('messages'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(messages), 1)
        self.assertEquals(messages[0].message, 'passwords do not match.')

    def test_register_user_POST_character_criterian_not_matched_in_password(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'test2',
            'last_name': 'user2',
            'user_name': 'test_user2',
            'email': 'test2@travelpedia.com',
            'pass1': 'Test123',
            'pass2': 'Test123',
        }, follow = True)

        messages = list(response.context.get('messages'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(messages), 1)
        self.assertEquals(messages[0].message, 'password should contain atleast a number, must contain atleast 8 characters,'
                                    + ' an special character, a lowercase and an uppercase letter.')

    def test_user_login_GET(self):
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_user_login_POST_success(self):
        response = self.client.post(reverse('login'), {
            'user_name': 'test_user',
            'pass': 'testpass'
        })
        
        self.assertEquals(response.status_code, 302)

    def test_user_login_POST_username_or_password_not_matched(self):
        response = self.client.post(reverse('login'), {
            'user_name': 'test_user_fake',
            'pass': 'testpass_fake'
        }, follow = True)

        messages = list(response.context.get('messages'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(messages), 1)
        self.assertEquals(messages[0].message, "Username or password didn't match")