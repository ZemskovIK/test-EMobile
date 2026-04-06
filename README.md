# 🔐 Auth & RBAC System

Собственная система аутентификации и авторизации на базе FastAPI.

## 🔒 Схема управления доступом

Система построена на ролевой модели (RBAC), но с гибким маппингом ресурсов и действий. Это позволяет управлять правами динамически через БД.

### 🛢 Структура базы данных
| Таблица | Описание |
|---------|----------|
| `users` | Аккаунты пользователей. Поле `is_active=False` используется для мягкого удаления. |
| `roles` | Роли пользователей (например, `admin`, `manager`). |
| `permissions` | Элементарные права доступа вида `resource:action` (например, `reports:read`). |
| `role_permissions` | Связь многие-ко-многим: какие права назначены какой роли. |
| `user_roles` | Связь многие-ко-многим: какие роли назначены какому пользователю. |
| `revoked_tokens` | Чёрный список отозванных refresh-токенов (для реализации Logout). |

### Логика проверки доступа

1. **Аутентификация (401):** Клиент передает JWT в заголовке `Authorization: Bearer <token>`. Зависимость `get_current_user` проверяет подпись токена и наличие активного пользователя в БД (`is_active=True`).
2. **Авторизация (403):** Зависимость `require_permission(resource, action)` выполняет JOIN-запрос к таблицам прав. Если связка `User -> Role -> Permission` не найдена, доступ запрещается.

## 🛠 Технологии
- **Framework**: FastAPI
- **Database**: PostgreSQL + AsyncSQLAlchemy 2.0
- **Auth**: PyJWT (access + refresh tokens), bcrypt (passlib)
- **Validation**: Pydantic v2
- **Migrations**: Alembic

## 🚀 Запуск проекта

1. **Установка зависимостей**:
```bash
pip install -r requirements.txt
```

2. **Настройка окружения:**
Скопируйте `.env.example` в `.env`, настройте `DATABASE_URL` и `SECRET_KEY`
```env
DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/your_db"
SECRET_KEY="your_secret_key"
```

3. **Миграции и сидинг:**
```bash
alembic upgrade head
python -m scripts.seed
```

4. **Запуск**
```bash
uvicorn app.main:app --reload
```

## 📡 API Endpoints

### Auth
- `POST /auth/register` — регистрация нового пользователя
- `POST /auth/login` — вход, получение пары токенов
- `POST /auth/logout` — выход (отзыв refresh-токена)
- `POST /auth/refresh` — обновление пары токенов

### Profile
- `GET /users/profile` — получение данных текущего пользователя
- `PATCH /users/profile` — обновление профиля (частичное)
- `DELETE /users/profile` — мягкое удаление аккаунта

### Admin (RBAC Management)
- `POST /admin/access/roles` — создать роль (требуется access_control:manage)
- `POST /admin/access/permissions` — создать право (требуется access_control:manage)
- `POST /admin/access/assign` — назначить право роли (требуется access_control:manage)

### Mock Resources (для демонстрации)
- `GET /api/v1/reports` — пример ресурса с правом `reports:read`
- `POST /api/v1/analytics` — пример ресурса с правом `analytics:write`

## 🧪 Тестирование

После запуска сидинга доступны следующие аккаунты:

| Email | Password | Role | Доступные права (пример) |
|-------|----------|------|--------------------------|
| admin@test.com | admin123 | Admin | Все ресурсы (`*:*`) |
| manager@test.com | mgr123 | Manager | `reports:read`, `analytics:write` |

### Сценарий проверки

1. **POST /auth/login** под менеджером → получаем токены.
2. **GET /api/v1/reports** с токеном менеджера -> `200 OK` (есть право `reports:read`).
3. **POST /admin/access/roles** с токеном менеджера -> `403 Forbidden` (нет права `access_control:manage`).
4. **DELETE /users/profile** -> `204 No Content` (аккаунт деактивирован).
5. Любой запрос с тем же токеном -> `401 Unauthorized` (пользователь `is_active=False`).

## 📂 Структура проекта
```
├── app/
│   ├── auth.py              # JWT, хеширование, get_current_user
│   ├── config.py            # Настройки из .env
│   ├── database.py          # AsyncEngine, сессии, Base
│   ├── db_depends.py        # get_async_db
│   ├── dependencies.py      # require_permission (фабрика зависимостей)
│   ├── main.py              # Точка входа
│   ├── models/              # SQLAlchemy модели (users, access)
│   ├── routers/             # Эндпоинты (auth, users, access_control, mock)
│   ├── schemas/             # Pydantic схемы валидации
│   └── migrations/          # Alembic
├── scripts/
│   └── seed.py              # Заполнение тестовыми данными
├── alembic/                 # Миграции
├── .env.example             # Шаблон переменных окружения
├── requirements.txt         # Зависимости
└── README.md                # Этот файл
```