FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD bash -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn qrcode_project.wsgi:application --bind 0.0.0.0:\$PORT"