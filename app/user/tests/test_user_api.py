from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_test_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            "email": "create_user@example.com",
            "password": "createuserpass123",
            "name": "userTest",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_create_user_with_email_error(self):
        payload = {
            "email": "create_user@example.com",
            "password": "createuserpass123",
            "name": "userTest",
        }

        create_test_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_is_short_error(self):
        """test if the password length is less than 5"""
        payload = {
            "email": "create_user@example.com",
            "password": "123",
            "name": "userTest",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user)

    def create_token_for_user(self):
        user_details = {
            "email": "create_user@example.com",
            "password": "createuserpass123",
            "name": "userTest",
        }
        create_test_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"]
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertContains("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        create_test_user(email="test@example.com", password="goodpass")

        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {"email": "test@example.com", "password": "pass123"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPiTest(TestCase):
    def setUp(self):
        self.user = create_test_user(
            email="private_user@gmail.com",
            password="private_user123",
            name="private user",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "name": self.user.name,
                "email": self.user.email
            }
        )

    def test_post_me_not_allowed(self):
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {
            "name": "new name",
            "password": "newPass123",
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
