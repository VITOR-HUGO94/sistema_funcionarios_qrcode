# Sistema de Funcionários com QRCode

Este é um projeto Django para gerenciamento de funcionários, com CRUD completo e integração de QRCode. Cada funcionário cadastrado pode ter um QRCode gerado que, ao ser lido, direciona para a página de detalhes do funcionário. O projeto está containerizado com Docker e pronto para rodar localmente ou em produção.

---

## Funcionalidades

- Cadastro, visualização, atualização e exclusão de funcionários.
- Autenticação de usuários personalizados (`SiteUser`).
- Geração e leitura de QRCode para cada funcionário.
- Frontend simples com Bootstrap.
- Containerizado com Docker e Docker Compose.
- Suporte a PostgreSQL como banco de dados.

---

## Pré-requisitos

- Docker
- Docker Compose
- Git (para clonar o repositório)

---

## Instalação

1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd sistema_qrcode_v2
Configure variáveis de ambiente criando um arquivo .env:

env
Copiar código
DATABASE_URL=postgres://user:pass@db:5432/qrcodedb
REDIS_URL=redis://redis:6379/0
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=qrcodedb
DJANGO_SECRET_KEY=sua-chave-super-secreta-aqui
DJANGO_DEBUG=True
Build e suba os containers Docker:

bash
Copiar código
docker-compose up --build
Acesse o container web para aplicar migrations e criar superusuário:

bash
Copiar código
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
A aplicação estará disponível em:

arduino
Copiar código
http://localhost:8000/
Estrutura do Projeto
csharp
Copiar código
sistema_qrcode_v2/
│
├── employees/           # App de funcionários
├── qrcode_project/      # Configurações do Django
├── templates/           # Templates HTML
├── static/              # Arquivos estáticos
├── venv/                # Virtual environment (ignorável pelo Git)
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── requirements.txt
Uso do QRCode
Cada funcionário possui um QRCode que direciona para a página de detalhes.

Para simular a leitura do QRCode localmente, você pode usar qualquer leitor de QRCode online ou biblioteca Python (qrcode / opencv).

Comandos úteis
Rodar servidor Django localmente:

bash
Copiar código
docker-compose exec web python manage.py runserver 0.0.0.0:8000
Criar superusuário:

bash
Copiar código
docker-compose exec web python manage.py createsuperuser
Aplicar migrations:

bash
Copiar código
docker-compose exec web python manage.py migrate
Acessar shell do Django:

bash
Copiar código
docker-compose exec web python manage.py shell
Tecnologias utilizadas
Django 5.x

Python 3.12

PostgreSQL 15

Docker & Docker Compose

Bootstrap 5

Biblioteca qrcode para geração de QR Codes

Contribuição
Pull requests são bem-vindos. Para mudanças maiores, abra uma issue primeiro para discutir o que deseja alterar.