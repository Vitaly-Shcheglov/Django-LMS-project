from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,  IsAuthenticated
from .models import CustomUser
from .serializers import UserProfileSerializer, PaymentSerializer, UserSerializer
from django.http import HttpResponse


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


def home(request):
    return HttpResponse("Welcome to the LMS!")


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id', None)
        lesson_id = self.request.query_params.get('lesson_id', None)
        payment_method = self.request.query_params.get('payment_method', None)

        if course_id:
            queryset = queryset.filter(paid_course_id=course_id)
        if lesson_id:
            queryset = queryset.filter(paid_lesson_id=lesson_id)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
            return super().get_permissions()
