from django.urls import path, include
from .views import CourseViewSet, LessonListCreate, LessonDetail
from rest_framework.routers import DefaultRouter

app_name = 'courses'


urlpatterns = [
    path('', CourseViewSet.as_view({'get': 'list'}), name='course-list'),
    path('lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
]
