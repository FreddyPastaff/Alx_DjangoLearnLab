
# blog/tests/test_auth.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthFlowTests(TestCase):
    def test_register_creates_user_and_logs_in(self):
        resp = self.client.post(reverse("blog:register"), {
            "username": "freddy",
            "email": "freddy@example.com",
            "password1": "S3curePass!123",
            "password2": "S3curePass!123",
        })
        self.assertRedirects(resp, reverse("blog:profile"))
        self.assertTrue(User.objects.filter(username="freddy").exists())

    def test_login_required_for_profile(self):
        resp = self.client.get(reverse("blog:profile"))
        self.assertRedirects(resp, f"{reverse('blog:login')}?next={reverse('blog:profile')}")

    def test_profile_update(self):
        user = User.objects.create_user("freddy", "f@x.com", "pass12345!")
        self.client.login(username="freddy", password="pass12345!")
        resp = self.client.post(reverse("blog:profile"), {
            "first_name": "Fred",
            "last_name": "D",
            "email": "freddy2@example.com",
        })
        self.assertRedirects(resp, reverse("blog:profile"))
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Fred")
        self.assertEqual(user.email, "freddy2@example.com")
