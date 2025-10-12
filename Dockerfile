FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências do sistema para PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Criar script para criar superusuário
RUN echo '#!/bin/bash\n\
python manage.py migrate --noinput\n\
python manage.py collectstatic --noinput\n\
if [ "$CREATE_SUPERUSER" = "True" ]; then\n\
    echo "Criando superusuário..."\n\
    python manage.py shell -c "\n\
from employees.models import SiteUser\n\
import os\n\
username = os.environ.get('\''DJANGO_SUPERUSER_USERNAME'\'')\n\
email = os.environ.get('\''DJANGO_SUPERUSER_EMAIL'\'')\n\
password = os.environ.get('\''DJANGO_SUPERUSER_PASSWORD'\'')\n\
if username and email and password:\n\
    if not SiteUser.objects.filter(username=username).exists():\n\
        SiteUser.objects.create_superuser(username=username, email=email, password=password)\n\
        print(f\"Superusuário {username} criado com sucesso!\")\n\
    else:\n\
        print(\"Superusuário já existe\")\n\
else:\n\
    print(\"Variáveis de ambiente do superusuário não definidas\")\n\
"\n\
fi\n\
gunicorn qrcode_project.wsgi:application --bind 0.0.0.0:$PORT --workers 3' > /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/bin/bash", "/app/start.sh"]