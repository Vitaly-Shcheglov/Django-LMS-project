from rest_framework import serializers
from .models import Course, Lesson, Subscription


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Course.

    Этот сериализатор преобразует объекты Course в JSON и обратно.
    Включает поле для подсчета количества уроков и вложенный сериализатор для уроков.
    """
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)


    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lesson_count', 'lessons']

    def get_is_subscribed(self, obj):
        """
        Проверяет, подписан ли текущий пользователь на курс.

        Args:
            obj (Course): Экземпляр курса.

        Returns:
            bool: True, если пользователь подписан на курс, иначе False.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Lesson.

    Этот сериализатор преобразует объекты Lesson в JSON и обратно.
    """
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_url']
        extra_kwargs = {
            'video_url': {
                'validators': [validate_video_url]
            }
        }


    def get_lesson_count(self, obj):
        """
        Возвращает количество уроков, связанных с курсом.

        Args:
            obj (Course): Экземпляр курса для которого необходимо получить количество уроков.

        Returns:
            int: Количество уроков, связанных с данным курсом.
        """
        return obj.lessons.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Subscription.

    Позволяет преобразовать объекты Subscription в JSON и обратно.
    """
    class Meta:
        model = Subscription
        fields = ['user', 'course']
