from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from .paginators import CustomPageNumberPagination


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.

    Позволяет создавать, просматривать, обновлять и удалять курсы.
    Доступ к операциям контролируется правами модераторов и авторизованных пользователей.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        """
        Определяет права доступа на основе действия.

        Returns:
            list: Список разрешений, которые будут применены к текущему действию.
        """
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve', 'update']:
            self.permission_classes = [IsModerator | permissions.IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Привязывает создаваемый курс к авторизованному пользователю.

        Args:
            serializer (CourseSerializer): Сериализатор для создания курса.
        """
        serializer.save(owner=self.request.user)


class LessonListCreate(generics.ListCreateAPIView):
    """
    View для списка и создания уроков.

    Позволяет пользователям просматривать список всех уроков и создавать новые.
    Использует фильтрацию и сортировку.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['course']
    ordering_fields = ['title', 'payment_date']
    ordering = ['title']


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View для получения, обновления и удаления конкретного урока.

    Позволяет пользователям просматривать, изменять или удалять урок по его ID.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления уроками.

    Позволяет создавать, просматривать, обновлять и удалять уроки.
    Доступ к операциям контролируется правами владельцев и модераторов.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        Определяет права доступа на основе действия.

        Returns:
            list: Список разрешений, которые будут применены к текущему действию.
        """
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['list', 'retrieve', 'update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return super().get_permissions()


class SubscriptionView(APIView):
    """
    View для управления подписками пользователей на курсы.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает создание или удаление подписки на курс.

        Args:
            request (Request): Объект запроса с данными о подписке.

        Returns:
            Response: Ответ с сообщением о статусе подписки.
        """
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
