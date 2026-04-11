# Cable_Base
Backend for cable manufacturing management. Built with FastAPI, SQLAlchemy, PostgreSQL, and Alembic. Provides API for cable specifications, inventory, and production workflow. Telegram bot interface (Aiogram) in development for production floor operations.


📋 Описание проекта

Cable_Base - это система управления кабельной базой данных, предназначенная для учета, хранения и анализа информации о кабельной продукции на предприятиях.
🚀 Основные возможности

    📊 Учет кабельной продукции и материалов

    🔍 Поиск и фильтрация кабелей по параметрам

    👥 Управление пользователями и правами доступа (в разработке)

🛠 Технологический стек

    Backend: Python (FastAPI)

    Frontend: aiogram

    База данных: PostgreSQL

    Контейнеризация: Docker (в разработке)

📁 Структура проекта

```text
Cable_Base/
├── infra/                  # контенеризация
│   ├── .env.production
│   └── docker-compose.yml
├── app/                    # Серверная часть приложения
│   ├── alembic/            # миграции
│   ├── api/                # блок API (эндпоинты, валидаторы)
│   ├── core/               # конфигурации системы
│   ├── crud/               # CRUD операции
│   ├── models/             # модели
│   ├── schemas/            # Pydantic схемы
│   ├── __init__.py/ 
│   └── main.py/            # точка входа
├── bot/                    # телеграм-бот
├── docker/                 # Docker конфигурации
├── requirements.txt        # Python зависимости
├── .env.example            # Пример переменных окружения
├── .env                    # переменные окружения
├── venv/                   # виртуальное окружение
├── requirements.txt        # зависимости
└── README.md             
```

⚡ Быстрый старт
Предварительные требования

    Python 3.12

    PostgreSQL 12+

    pip (менеджер пакетов Python)


Клонирование репозитория:

```bash
git clone git@github.com:MoiseevIgorPython/Cable_Base.git

cd cable_base
```

Создание виртуального окружения:

```bash
python -m venv venv
. venv/bin/activate  # для Linux/Mac
# или
. venv/Scripts/activate     # для Windows
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Настройка окружения:

```bash
cp .env.example .env
# Отредактируйте .env файл, указав свои настройки БД
```

Настройка базы данных:

```bash
alembic revision --autogenerate -m "message" # создание нового сценария
alembic upgrade head # применение миграций
```

Загрузить компоненты в БД:

```bash
python scripts/add_test_data.py
```

Запуск сервера:

```bash
cd app
uvicorn main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000

🐳 Запуск через Docker (в разработке)
Перейдите в директорию infra, добавьте данные для подклучения к базе в файл .env.production, и выполните команду docker compose up
```bash
cd infra
docker-compose up -d
```

📊 Модели данных
Основные сущности:

    Cable - основная информация о кабеле

    Construction - конструкция кабеля

    Twisting - скрученная металическая проволока


🔧 API Документация

После запуска сервера документация API доступна:

    Swagger UI: http://localhost:8000/swagger/

# Возможные проблемы:
При создании нового сценария миграций, необходимо вручную удалить строку создания Enum типов в БД:
```
sa.Enum('CABLE', 'TWIST', name='department').create(op.get_bind()) - удалить в функции upgrade
```
Без этого могут не выполниться миграции при развертывании через docker compose

Запуск бота:

```bash
python bot/bot.py
```

В боте настроена аутентификация, перед использованием необходимо создать пользователя, и залогинеться по email и password.


Админ-панель:

- Доступна по адресу localhost:8000/admin
- Доступ только у superuser (суперюзер создается при первом запуске)
