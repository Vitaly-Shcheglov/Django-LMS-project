from rest_framework import serializers
from .models import CustomUser, Payment
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CustomUser.

    Этот сериализатор преобразует объекты CustomUser в JSON и обратно.
    Позволяет создавать и обновлять пользователей, включая обработку пароля.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Создает нового пользователя с заданными данными.

        Args:
            validated_data (dict): Данные, валидированные сериализатором.

        Returns:
            User: Созданный объект пользователя.
        """
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.

    Этот сериализатор преобразует объекты Payment в JSON и обратно.
    Позволяет управлять платежами пользователей.
    """
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.

    Этот сериализатор преобразует объекты CustomUser в JSON и обратно.
    Включает информацию о платежах пользователя.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'city', 'avatar', 'payment_set']

    def get_payments(self, obj):
        """
        Получает все платежи, связанные с пользователем.

        Args:
            obj (CustomUser): Экземпляр пользователя для получения платежей.

        Returns:
            list: Сериализованные данные о платежах.
        """
        from .serializers import PaymentSerializer
        return PaymentSerializer(obj.payments.all(), many=True).data


class CustomRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.

    Этот сериализатор позволяет создавать нового пользователя
    с минимальным набором полей, необходимым для регистрации.
    """
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Создает нового пользователя на основе валидированных данных.

        Args:
            validated_data (dict): Данные, валидированные сериализатором.

        Returns:
            CustomUser: Созданный объект пользователя.
        """
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
