from django.core.exceptions import ValidationError
from urllib.parse import urlparse


class ExternalLinkValidator:
    """
    Валидатор для проверки, что ссылка ведет только на youtube.com.
    """

    def __init__(self, field):
        """
        Инициализирует валидатор с указанным полем.

        Args:
            field (str): Имя поля, которое будет валидироваться.
        """
        self.field = field

    def __call__(self, attrs):
        """
        Проверяет, что ссылка в указанном поле ведет на youtube.com.

        Args:
            attrs (dict): Словарь атрибутов, содержащий данные для проверки.

        Raises:
            ValidationError: Если ссылка не ведет на youtube.com.
        """
        url = attrs.get(self.field)
        if url is not None:
            parsed_url = urlparse(url)
            if parsed_url.netloc != "www.youtube.com" and parsed_url.netloc != "youtube.com":
                raise ValidationError(f"Ссылка в поле {self.field} должна вести только на youtube.com")
