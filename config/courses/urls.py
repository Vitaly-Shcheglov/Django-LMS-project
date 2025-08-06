from django.urls import path
from .views import CourseViewSet, LessonListCreate, LessonDetail, SubscriptionView, CourseUpdateView


app_name = "courses"


urlpatterns = [
    path("", CourseViewSet.as_view({"get": "list"}), name="course-list"),
    path("<int:pk>/", CourseUpdateView.as_view(), name="course-update"),
    path("lessons/", LessonListCreate.as_view(), name="lesson-list-create"),
    path("lessons/<int:pk>/", LessonDetail.as_view(), name="lesson-detail"),
    path("subscriptions/", SubscriptionView.as_view(), name="subscription"),
]
