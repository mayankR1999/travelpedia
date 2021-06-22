from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Posts, UserDetails
from . import views
import tempfile, os

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


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create_user(username = 'test_user', email = 'test@travelpedia.com',
                    password = 'testpass', first_name = 'test', last_name = 'user')
        self.user1_details = UserDetails.objects.create(user=self.user1, user_description='test description')

        self.post1 = Posts.objects.create(owner = self.user1, experience='test experience', place='test place',
                    img=tempfile.NamedTemporaryFile(suffix=".jpg").name)
        
        self.post1.create_timestamp()

        print(self.post1.img.url)

        self.client.login(username='test_user', password='testpass')
        
    def test_user_feed(self):
        response = self.client.get(reverse('user_feed'))
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user-feed.html')

    def test_post_upload_GET(self):
        response = self.client.get(reverse('post_upload'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload.html')

    def test_post_upload_POST(self):
        response = self.client.post(reverse('post_upload'), {
            'place': 'test place 2',
            'exp': 'test experience 2',
            'image': tempfile.NamedTemporaryFile(suffix=".jpg")
        })

        self.assertEquals(response.status_code, 302)
        os.remove()

    def test_search_post(self):
        response = self.client.post(reverse('searchPost'), {
            'searchKey': 'test place'
        }, follow = True)

        post = list(response.context.get('posts'))[0]

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user-feed.html')
        self.assertEquals(post.place, 'test place')
        self.assertEquals(post.experience, 'test experience')

    def test_post_like(self):
        response = self.client.get(reverse('like_post'), {
            'post_id': self.post1.id
        }, follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.post1.count_likes(), 1)

    def test_show_user_profile(self):
        response = self.client.get(reverse('show_user_profile', args = [self.user1.id]), follow = True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'user-profile.html')

    def test_chenge_dp(self):
        response = self.client.post(reverse('change_dp'), {
            'pic': tempfile.NamedTemporaryFile(suffix=".jpg")
        })

        self.assertEquals(response.status_code, 302)

    def test_change_bio(self):
        response = self.client.post(reverse('change_bio'), {
            'text': 'sample bio'
        })

        self.assertEquals(response.status_code, 200)

    def test_follow_toggle(self):
        new_user = User.objects.create_user(username = 'test_user2', email = 'test2@travelpedia.com',
                    password = 'testpass2', first_name = 'test2', last_name = 'user2')
        new_user_details = UserDetails.objects.create(user=new_user, user_description='test description 2')

        response = self.client.get(reverse('follow_toggle_request'), {
            'user_id': new_user.id,
            'request_type': 'follow'
        })

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(new_user_details.followers.all()), 1)
        self.assertEquals(len(self.user1_details.following.all()), 1)
    