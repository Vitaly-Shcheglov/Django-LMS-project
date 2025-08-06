from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()


class CourseLessonTests(APITestCase):
    """
    Тесты для проверки CRUD операций с уроками и подписками на курсы.
    """

    def setUp(self):
        """
        Настройка тестовых данных.
        """
        self.moderator = User.objects.create_user(
            email="moderator@example.com", password="password123", phone="1234567890", city="CityName"
        )
        self.user = User.objects.create_user(
            email="user@example.com", password="password123", phone="0987654321", city="AnotherCity"
        )

        self.course = Course.objects.create(
            title="Test Course", description="Description for test course", owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title="Test Lesson", description="Description for test lesson", course=self.course, owner=self.user
        )

        self.client.force_authenticate(user=self.moderator)

    def test_create_lesson(self):
        """
        Проверка создания урока.
        """
        url = reverse("lesson-list")
        data = {
            "title": "New Lesson",
            "description": "New lesson description",
            "course": self.course.id,
            "owner": self.user.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson(self):
        """
        Проверка обновления урока.
        """
        url = reverse("lesson-detail", args=[self.lesson.id])
        data = {"title": "Updated Lesson", "description": "Updated description", "course": self.course.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        """
        Проверка удаления урока.
        """
        url = reverse("lesson-detail", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscription_to_course(self):
        """
        Проверка подписки на курс.
        """
        url = reverse("subscription")
        data = {"course_id": self.course.id}
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
