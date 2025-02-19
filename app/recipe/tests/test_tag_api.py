from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from core.models import Tag

from rest_framework.test import APIClient
from rest_framework import status

from recipe.serializers import TagSerializer


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
