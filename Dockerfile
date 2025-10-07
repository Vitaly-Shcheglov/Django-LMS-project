FROM python:3.12-slim


WORKDIR /app


RUN apt-get update \
    && apt-get install -y libgssapi-krb5-2 libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


RUN mkdir -p /app/staticfiles


EXPOSE 8000


CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]