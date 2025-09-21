# Yatube API

REST API для соцсети Yatube: публикации, комментарии, группы и подписки. Поддерживается регистрация/аутентификация по JWT-токенам, пагинация, фильтрация и разграничение прав доступа.

## Быстрый старт (локально)
1) Клонируйте репозиторий
`git clone https://github.com/IbodovAziz/api-final-yatube.git`

2) Создайте и активируйте виртуальное окружение
`python -m venv .venv`
Windows: .venv\Scripts\activate
Linux/macOS:
source .venv/bin/activate

3) Установите зависимости
`pip install -r requirements.txt`

4) Примените миграции
`python manage.py migrate`

5) (Опционально) создайте суперпользователя
`python manage.py createsuperuser`

6) Запустите сервер
`python manage.py runserver`

## Получение токена
Получение токена по логину/паролю пользователя:
POST `/api/v1/jwt/create/`

Ответ:
`{
  "refresh": "…",
  "access": "…"
}`

# Основные эндпоинты

## Посты

* `GET /api/v1/posts/` — список постов.

* `POST /api/v1/posts/` — создать пост (только аутентифицированные).

* `GET /api/v1/posts/{id}/` — получить пост.

* `PUT/PATCH /api/v1/posts/{id}/` — изменить свой пост.

* `DELETE /api/v1/posts/{id}/` — удалить свой пост.

## Комментарии

* `GET /api/v1/posts/{post_id}/comments/`

* `POST /api/v1/posts/{post_id}/comments/ (только аутентифицированные)` 

* `GET /api/v1/posts/{post_id}/comments/{id}/`

* `PUT/PATCH /api/v1/posts/{id}/`

* `PATCH/DELETE /api/v1/posts/{post_id}/comments/{id}/`

## Группы

* `GET /api/v1/groups/` — список групп.

* `GET /api/v1/groups/{id}/` — детальная информация о группе.

## Подписки

* `GET /api/v1/follow/` — список подписок текущего пользователя.

* `POST /api/v1/follow/` — подписаться на автора.

## Права доступа и поведение

* Создавать/редактировать/удалять посты и комментарии может только автор.

* Просматривать — любой пользователь.

* Подписываться — только аутентифицированные.

* Для небезопасных методов требуется заголовок Authorization.

## Пагинация и фильтрация

* Пагинация стандартная DRF (limit/offset или page — зависит от настроек).

* Фильтрация/поиск для подписок и постов (например, по автору) — через query-параметры, если включено в вьюсетах.
