from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson


class CustomUser(AbstractUser):
    """
    Пользовательская модель пользователя, наследующая от AbstractUser.

    Включает дополнительные поля:
    - email: уникальный адрес электронной почты.
    - phone: номер телефона пользователя.
    - city: город проживания.
    - avatar: изображение профиля пользователя.

    Поля username и REQUIRED_FIELDS настроены для использования email в качестве имени пользователя.
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'city']

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
    )


class Payment(models.Model):
    """
    Модель платежа, связанная с пользователем и курсом.

    Атрибуты:
    - user: пользователь, совершивший платеж.
    - payment_date: дата и время, когда был совершен платеж.
    - paid_course: курс, за который был осуществлен платеж (может быть пустым).
    - paid_lesson: урок, за который был осуществлен платеж (может быть пустым).
    - amount: сумма платежа.
    - payment_method: метод оплаты (наличные или перевод на счет).
    """
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey('courses.Course', null=True, blank=True, on_delete=models.CASCADE)
    paid_lesson = models.ForeignKey('courses.Lesson', null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        """
        Возвращает строковое представление платежа.

        Returns:
            str: Информация о платеже, включая имя пользователя, сумму и метод платежа.
        """
        return f"{self.user.username} - {self.amount} - {self.payment_method}"
