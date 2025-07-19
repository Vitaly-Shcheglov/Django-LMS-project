from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def validate_video_url(value):
    """
    Проверка, что ссылка на видео ведет на youtube.com.

    Args:
        value (str): Ссылка, которую необходимо проверить.

    Raises:
        ValidationError: Если ссылка не ведет на youtube.com.
    """
    parsed_url = urlparse(value)
    if parsed_url.netloc != 'www.youtube.com' and parsed_url.netloc != 'youtube.com':
        raise ValidationError('Ссылка должна вести на youtube.com')
