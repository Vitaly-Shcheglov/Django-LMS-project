from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User


class Command(BaseCommand):
    help = 'Создает группу модераторов, назначает ей права и добавляет пользователей в группу'

    def handle(self, *args, **kwargs):
        group_name = 'Moderators'

        group, created = Group.objects.get_or_create(name=group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана.'))
        else:
            self.stdout.write(self.style.WARNING(f'Группа "{group_name}" уже существует.'))

        permissions = [
            'view_course',
            'change_course',
            'view_lesson',
            'change_lesson',
        ]

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                group.permissions.add(permission)
                self.stdout.write(self.style.SUCCESS(f'Право "{perm}" добавлено в группу "{group_name}".'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Право "{perm}" не найдено.'))

        user_emails = ['moderator1@example.com',
                       'moderator2@example.com']  # Замените на фактический email зарегистрированного пользователя

        for email in user_emails:
            try:
                user = User.objects.get(email=email)
                user.groups.add(group)
                self.stdout.write(
                    self.style.SUCCESS(f'Пользователь "{user.username}" добавлен в группу "{group_name}".'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Пользователь с email "{email}" не найден.'))
