from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


def create_user(email="testuser@gmail.com", password="testpass123"):
    return get_user_model().objects.create_user(email=email, password=password)


class TestUserModel(TestCase):
    def test_create_user(self):
        email = "test_user@example.com"
        password = "test_user_pass123"

        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        emails = {
            "test1@EXAMPLE.com": "test1@example.com",
            "Test2@Example.com": "Test2@example.com",
            "TEST3@EXAMPLE.COM": "TEST3@example.com",
            "test4@example.COM": "test4@example.com",
        }
        for email, expected in emails.items():
            user = get_user_model().objects.create_user(email, "test123")
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_if_user_is_admin(self):
        user = get_user_model().objects.create_superuser(
            email="example@example.com",
            password="test123",
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            email="user@example.com", password="userpass123", name="username"
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="recipe name",
            time_minutes=5,
            price=Decimal("5.5"),
            description="sample recipe description",
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        user = create_user()

        tag = models.Tag.objects.create(user=user, name="tag1")
        self.assertEqual(str(tag), tag.name)
