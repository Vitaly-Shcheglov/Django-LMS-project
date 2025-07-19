from rest_framework import serializers
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.

    Этот сериализатор преобразует объекты Course в JSON и обратно.
    Включает поле для подсчета количества уроков и вложенный сериализатор для уроков.
    """
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lesson_count', 'lessons']


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.

    Этот сериализатор преобразует объекты Lesson в JSON и обратно.
    """
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url']

    def get_lesson_count(self, obj):
        """
        Возвращает количество уроков, связанных с курсом.

        Args:
            obj (Course): Экземпляр курса для которого необходимо получить количество уроков.

        Returns:
            int: Количество уроков, связанных с данным курсом.
        """
        return obj.lessons.count()
        