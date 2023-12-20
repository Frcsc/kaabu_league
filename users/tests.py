from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from users.models import UserProfile

User = get_user_model()


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(**self.user_data)
        self.assertEqual(superuser.email, self.user_data['email'])
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)


class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        self.user = User.objects.create_user(**self.user_data)

        self.profile_data = {
            'user': self.user,
            'type_of_user': UserProfile.USERTYPE.ADMIN_USESRS,
        }

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(**self.profile_data)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.type_of_user, UserProfile.USERTYPE.ADMIN_USESRS)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.profile = UserProfile.objects.create(user=self.user)

    def test_registration_view(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('registration'),
            {'new_email': 'newuser@example.com', 'new_password': 'newpassword'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

        self.client.login(**self.user_data)
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('games'))

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('login'),
            {'email': 'testuser@example.com', 'password': 'testpassword'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('games'))

        self.client.login(**self.user_data)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('games'))

    def test_logout_view(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
