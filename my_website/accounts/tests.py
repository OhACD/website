from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from .tokens import generate_login_token, generate_verification_token, verify_login_token, verify_verification_token


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class MagicLinkTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(email="user@example.com", name="User", is_verified=True)

    def test_login_token_single_use(self):
        token = generate_login_token(self.user.email)
        self.assertIsNotNone(verify_login_token(token))
        self.assertIsNone(verify_login_token(token))

    def test_verification_token_single_use(self):
        token = generate_verification_token(self.user.email)
        self.assertIsNotNone(verify_verification_token(token))
        self.assertIsNone(verify_verification_token(token))

    def test_login_rate_limit_blocks_after_threshold(self):
        url = reverse("accounts:login")
        data = {"email": self.user.email}

        for _ in range(5):
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, 200)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url)
