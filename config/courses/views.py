from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.

    Позволяет создавать, просматривать, обновлять и удалять курсы.
    Доступ к операциям контролируется правами модераторов и авторизованных пользователей.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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
