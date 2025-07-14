from django.urls import path, include
from .views import CourseViewSet, LessonListCreate, LessonDetail
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
path('lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
]
