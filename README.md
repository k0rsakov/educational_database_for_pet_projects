# educational_database_for_pet_projects
educational_database_for_pet_projects
## Создание виртуального окружения

```bash
python3.12 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install poetry && \
poetry lock && \
poetry install
```

## Разворачивание инфраструктуры

```bash
docker-compose up -d
```

## Quick Start

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your database credentials

3. Start the services:
   ```bash
   docker compose up -d
   ```

4. Connect to PostgreSQL through PgBouncer:
   ```bash
   psql -h localhost -p 5432 -U your_username -d postgres
   ```
