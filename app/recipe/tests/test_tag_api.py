from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from core.models import Tag,Recipe

from rest_framework.test import APIClient
from rest_framework import status

from recipe.serializers import TagSerializer

from decimal import Decimal

def create_user(email="tset_user@gmail.com", password="testpass123"):
    return get_user_model().objects.create_user(email=email, password=password)


def detailed_url(tag_id):
    return reverse("recipe:tag-detail", args=[tag_id])


TAG_URL = reverse("recipe:tag-list")


class PublicTagTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_all_tags(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTestTags(TestCase):
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_all_tags(self):
        Tag.objects.create(user=self.user, name="tag1")
        Tag.objects.create(user=self.user, name="tag2")

        tags = Tag.objects.all().order_by("name")
        ser = TagSerializer(tags, many=True)
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser.data)

    def test_retrieve_user_tags(self):
        other_user = create_user(
            email="other_usre@test.com",
            password="otherpass123"
        )
        Tag.objects.create(user=self.user, name="tag1")
        Tag.objects.create(user=self.user, name="tag2")
        Tag.objects.create(user=other_user, name="tag3")

        res = self.client.get(TAG_URL)
        tags = Tag.objects.filter(user=self.user)

        ser = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, ser.data)

    def test_update_partial_tag(self):
        tag = Tag.objects.create(user=self.user, name="tagToUpdate")
        payload = {"name": "nameUpdated"}
        res = self.client.patch(detailed_url(tag.id), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_deleting_tag(self):
        tag = Tag.objects.create(user=self.user, name="destroy_tag")
        res = self.client.delete(detailed_url(tag.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tag = Tag.objects.filter(user=self.user)
        self.assertFalse(tag.exists())

    def test_filter_tags_assigned_to_recipes(self):
        """Test listing tags to those assigned to recipes."""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Green Eggs on Toast',
            time_minutes=10,
            price=Decimal('2.50'),
            user=self.user,
        )
        recipe.tags.add(tag1)

        res = self.client.get(TAG_URL, {'assigned_only': 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test filtered tags returns a unique list."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Dinner')
        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minutes=5,
            price=Decimal('5.00'),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minutes=3,
            price=Decimal('2.00'),
            user=self.user,
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(TAG_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
