from celery import shared_task
from django.utils import timezone
from .models import Course
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def notify_users_about_upcoming_courses():
    """
    Периодическая задача для уведомления пользователей о курсах, начинающихся в ближайшие 24 часа.
    """
    now = timezone.now()
    upcoming_courses = Course.objects.filter(start_date__gt=now, start_date__lt=now + timezone.timedelta(days=1))

    users = User.objects.all()

    for user in users:
        user_courses = upcoming_courses.filter(owner=user)
        if user_courses.exists():
            course_titles = ", ".join(course.title for course in user_courses)

            send_mail(
                subject="Уведомление о курсах",
                message=f"У вас начинаются курсы: {course_titles}.",
                from_email="no-reply@example.com",  # Замените на ваш адрес отправителя
                recipient_list=[user.email],
                fail_silently=False,
            )

            print(f"Уведомление отправлено пользователю {user.email}: У вас начинаются курсы: {course_titles}.")


@shared_task
def send_course_update_email(course_title, user_email):
    """
    Асинхронная задача для отправки уведомления о обновлении курса.

    Args:
        course_title (str): Заголовок обновленного курса.
        user_email (str): Электронная почта пользователя, которому отправляется уведомление.
    """
    subject = f"Обновление курса: {course_title}"
    message = f'Курс "{course_title}" был обновлен. Проверьте обновления на сайте.'
    send_mail(
        subject=subject,
        message=message,
        from_email="no-reply@example.com",  # Замените на ваш адрес отправителя
        recipient_list=[user_email],
        fail_silently=False,
    )
