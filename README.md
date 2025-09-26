# Questions and Answers API (DRF and FastAPI)

Небольшой проект с реализацией API, используя Django REST Framework и FastAPI. 
API позволяет создавать вопросы и ответы, 
получать список вопросов, детально просматривать вопрос с ответами 
и каскадно удалять связанные записи.

## Запуск на новом устройстве

### 1. Клонировать репозиторий
```bash
git clone https://github.com/mayflowerr/test-task.git
cd <папка_репозитория>
```

### 2. Собрать и запустить контейнеры
```bash
docker compose build
docker compose up -d
docker compose ps
```

**Если нужно запустить что-то одно, сперва запуск сервера базы данных:**
```bash
docker compose up -d db
```

**Если нужно запустить только DRF:**
```bash
docker compose up -d drf
docker compose exec drf python manage.py migrate
```

**Только FastAPI:**
```bash
docker compose up -d fastapi
```

### 3. Инициализировать базы данных

**Django:**
```bash
docker compose exec drf python manage.py migrate
```

**FastAPI:**  
Таблицы создаются автоматически при старте.

---

## Проверка работы

- DRF: [http://localhost:8000/questions/](http://localhost:8001/questions/)  
- FastAPI: [http://localhost:8001/questions/](http://localhost:8000/questions/)  
- FastAPI Swagger UI: [http://localhost:8001/docs](http://localhost:8000/docs)  

---

## Запуск тестов

**DRF:**
```bash
docker compose exec drf pytest -q
```

**FastAPI:**
```bash
docker compose exec fastapi pytest -q
```