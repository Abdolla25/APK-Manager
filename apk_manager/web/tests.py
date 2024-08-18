from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UserAuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpass",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("profile"))

    def test_logout(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)


class ViewTests(TestCase):

    def test_homepage_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "APK Manager")

    def test_language_switcher(self):
        response = self.client.post(reverse("set_language"), {"language": "fr"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Bienvenue sur Apk Manager", response.content)
