from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, Payment
from .services import create_product, create_price, create_checkout_session
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import UserProfileSerializer, PaymentSerializer, UserSerializer, CustomUserSerializer, CustomRegisterSerializer
from django.http import HttpResponse


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View для получения и обновления профиля пользователя.

    Доступен только для авторизованных пользователей.
    Позволяет пользователю просматривать и изменять свои данные.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Получает текущего пользователя.

        Returns:
            CustomUser: Объект текущего пользователя.
        """
        return self.request.user


class UserListView(generics.ListAPIView):
    """
    View для получения списка всех пользователей.

    Доступен только для авторизованных пользователей.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


def home(request):
    """
    Главная страница.

    Возвращает приветственное сообщение.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Приветственное сообщение.
    """
    return HttpResponse("Welcome to the LMS!")


class PaymentListView(generics.ListAPIView):
    """
    View для получения списка всех платежей.

    Доступен только для авторизованных пользователей.
    Позволяет фильтровать платежи по курсу, уроку и методу оплаты.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает отфильтрованный список платежей на основе параметров запроса.

        Args:
            None

        Returns:
            QuerySet: Отфильтрованный список платежей.
        """
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


class PaymentCreateView(APIView):
    """
    View для создания платежа.

    Позволяет пользователю создать платеж за курс, создавая продукт и цену в Stripe,
    а также сессию для получения ссылки на оплату.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает создание платежа.

        Args:
            request (Request): Объект запроса с данными о платеже.

        Returns:
            Response: Ответ с информацией о платежной сессии.
        """
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        product = create_product(course.title, course.description)
        price = create_price(product.id, int(course.price * 100))

        session = create_checkout_session(price.id)

        Payment.objects.create(
            user=request.user,
            paid_course=course,
            amount=course.price,
            payment_method='stripe',
        )

        return Response({"url": session.url}, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями.

    Позволяет создавать, просматривать, обновлять и удалять пользователей.
    Доступ к созданию пользователей разрешен для неаутентифицированных пользователей,
    остальные действия доступны только для авторизованных пользователей.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Определяет права доступа на основе действия.

        Returns:
            list: Список разрешений, которые будут применены к текущему действию.
        """
        if self.action in ['create']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
            return super().get_permissions()


class RegisterView(viewsets.ModelViewSet):
    """
    ViewSet для регистрации новых пользователей.

    Позволяет пользователям регистрироваться в системе.
    Доступен для всех пользователей (включая неаутентифицированных).
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomRegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        """
        Создает нового пользователя.

        Args:
            request (Request): Объект запроса с данными для создания пользователя.

        Returns:
            Response: Ответ с данными созданного пользователя и статусом 201.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View для получения JWT токена.

    Позволяет пользователям получать токен для аутентификации.
    Доступен для всех пользователей (включая неаутентифицированных).
    """
    permission_classes = []
