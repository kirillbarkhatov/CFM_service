# CFM Service — учёт движения денежных средств (ДДС)

## Описание

CFM Service — это современное веб-приложение для учёта, анализа и управления движением денежных средств (ДДС) компании или частного лица. Позволяет вести учёт всех денежных операций с гибкой системой справочников и фильтрацией.

**Технологии:**
- Python, Django, Django ORM
- Bootstrap 5 (UI)
- PostgreSQL
- Docker, Docker Compose
- nginx

---

## Возможности
- Учёт всех операций ДДС: поступления, списания, категории, подкатегории, статусы
- Гибкое управление справочниками (статусы, типы, категории, подкатегории)
- Фильтрация по дате, статусу, типу, категории, подкатегории
- Удобный интерфейс на Bootstrap
- Импорт/экспорт данных через фикстуры
- Быстрый запуск через Docker Compose

---


## Быстрый старт

### 1. Клонируйте репозиторий
```sh
git clone https://github.com/kirillbarkhatov/CFM_service.git
cd CFM_service
```

### 2. Настройте переменные окружения
Создайте файл `.env` на основе `.env_sample_local` и укажите:
- `SECRET_KEY` — секретный ключ Django
- `DEBUG` — режим (True/False)
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` — параметры БД

### 3. Запуск через Docker Compose
```sh
docker-compose up --build
```
- Django будет доступен на [http://localhost:8000/](http://localhost:8000/)
- Админка: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### 4. Миграции и суперпользователь
```sh
docker-compose exec web python manage.py migrate

# создать суперпользователя:
docker-compose exec web python manage.py createsuperuser
```

---

## Работа с фикстурами

- **Выгрузить актуальные данные:**
  ```sh
  docker-compose exec web python manage.py dumpdata cfms.status cfms.type cfms.category cfms.subcategory --indent 2 > cfms/fixtures/initial_data.json
  ```
- **Загрузить справочники:**
  ```sh
  docker-compose exec web python manage.py load_initial_data
  ```

---

## Основные страницы

- `/` — список всех записей ДДС с фильтрами
- `/add/` — добавление новой записи
- `/edit/<id>/` — редактирование записи
- `/delete/<id>/` — удаление записи
- `/directories/` — управление справочниками (статусы, типы, категории, подкатегории)
- `/admin/` — стандартная админка Django

---

## Примеры интерфейса

- Таблица ДДС с фильтрами по дате, статусу, типу, категории, подкатегории
- Удобные формы создания/редактирования с зависимостями (категория зависит от типа, подкатегория — от категории)
- Управление справочниками через отдельную страницу и модальные окна

---

## Полезные команды

- **Собрать статику:**
  ```sh
  python manage.py collectstatic --noinput
  ```
- **Логи Docker:**
  ```sh
  docker-compose logs -f
  ```
- **Остановить проект:**
  ```sh
  docker-compose down
  ```

---

## Лицензия

MIT License