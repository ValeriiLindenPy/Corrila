from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from core.tests.profile_factory import ProfileFactory
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY
from users.forms import UserProfileCreationForm
from users.views import SignUpUser
from .models import Profile


class ProfileModelTestCase(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.test_user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.profile = Profile.objects.create(user=self.test_user, occupation="Tester")

    def test_profile_str_method(self):
        # Test the __str__ method of the Profile model
        self.assertEqual(str(self.profile), "testuser")

    def test_profile_get_absolute_url(self):
        # Test the get_absolute_url method of the Profile model
        expected_url = reverse("profile", kwargs={"user_id": self.test_user.pk})
        self.assertEqual(self.profile.get_absolute_url(), expected_url)


class SignUpUserTest(TestCase):
    def test_sign_up_success(self):
        # Create a POST request with form data for a new user
        form_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "occupation": "Software Engineer",
        }

        client = Client()
        response = client.post(reverse("sign-up"), form_data)

        # Check if the user is redirected to the correct URL upon successful sign-up
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("sign-in"))

        # Check if the user was created and logged in
        self.assertTrue(User.objects.filter(username="testuser").exists())
        user = User.objects.get(username="testuser")
        self.assertTrue(user.is_authenticated)
        self.assertEqual(int(client.session[SESSION_KEY]), user.pk)


class SignInUserTest(TestCase):
    def setUp(self):
        self.user: Profile = ProfileFactory.create()

    def test_sign_in_success(self):
        response = self.client.post(
            reverse("sign-in"),
            {"username": self.user.user.username, "password": self.user.user.password},
        )
        self.assertEqual(response.status_code, 200)
