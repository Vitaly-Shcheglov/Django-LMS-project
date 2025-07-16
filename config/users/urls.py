from django.urls import path
from .views import UserProfileView, UserListView

app_name = 'users'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', UserListView.as_view(), name='user-list'),
]
