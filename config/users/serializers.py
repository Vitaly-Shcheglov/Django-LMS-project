from rest_framework import serializers
from .models import CustomUser, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'city', 'avatar', 'payments']

    def get_payments(self, obj):
        from .serializers import PaymentSerializer
        return PaymentSerializer(obj.payments.all(), many=True).data
