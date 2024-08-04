from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from materials.models import Course, Lesson, Subscription

User = get_user_model()


class ApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title="Test Course",
            description="Test Description",
            owner=self.user,
            video_link="https://www.youtube.com/watch?v=example",
        )

    def test_course_crud(self):
        # Create
        response = self.client.post(
            "/courses/",
            {
                "title": "New Course",
                "description": "New Description",
                "video_link": "https://www.youtube.com/watch?v=example",
            },
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # debug
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Read
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update
        course_id = Course.objects.get(title="New Course").id
        response = self.client.put(
            f"/courses/{course_id}/",
            {
                "title": "Updated Course",
                "description": "Updated Description",
                "video_link": "https://www.youtube.com/watch?v=example",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete
        response = self.client.delete(f"/courses/{course_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscription(self):
        # Subscribe
        response = self.client.post("/subscribe/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check subscription
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

        # Unsubscribe
        response = self.client.post("/subscribe/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check unsubscription
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
