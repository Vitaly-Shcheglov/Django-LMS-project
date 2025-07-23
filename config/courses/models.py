from users.models import CustomUser
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Course(models.Model):
    """
    Модель курса.

    Атрибуты:
        title (str): Заголовок курса.
        preview (ImageField): Изображение для предпросмотра курса.
        description (TextField): Описание курса.
        owner (User): Владелец курса, связанный с моделью User.
    """
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление курса.

        Returns:
            str: Заголовок курса.
        """
        return self.title


class Lesson(models.Model):
    """
    Модель урока.

    Атрибуты:
        title (str): Заголовок урока.
        description (TextField): Описание урока.
        preview (ImageField): Изображение для предпросмотра урока.
        video_url (URLField): URL видео урока.
        course (Course): Курс, к которому принадлежит урок.
        owner (User): Владелец урока, связанный с моделью User.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_url = models.URLField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='lessons', on_delete=models.CASCADE)

    def __str__(self):
        """
        Возвращает строковое представление урока.

        Returns:
            str: Заголовок урока.
        """
        return self.title


class Subscription(models.Model):
    """
    Модель подписки на обновления курса.

    Атрибуты:
        user (ForeignKey): Пользователь, подписавшийся на курс.
        course (ForeignKey): Курс, на обновления которого подписан пользователь.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')
