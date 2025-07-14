from django.urls import path
from .views import UserProfileView, UserListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', UserListView.as_view(), name='user-list'),
]
