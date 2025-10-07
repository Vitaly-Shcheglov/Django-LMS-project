from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileView, UserListView, PaymentListView, PaymentCreateView
from .views import UserViewSet, RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"register", RegisterView, basename="register")

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("", UserListView.as_view(), name="user-list"),
    path("payments/", PaymentListView.as_view(), name="payment-list"),
    path("payments/create/", PaymentCreateView.as_view(), name="payment-create"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
