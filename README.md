# Document Search Service

Сервис полнотекстового поиска по документам. Документы хранятся в PostgreSQL, поисковый индекс — в Elasticsearch. Сервис умеет искать документы по произвольному текстовому запросу и удалять документ сразу из БД и из индекса.

## Стек

* Python 3.12 
* FastAPI
* PostgreSQL 16
* Elasticsearch 8.19 
* SQLAlchemy (async)
* pytest
* Docker

Полный список зависимостей — в `requirements.txt`. 

## Структура проекта

    doc-search/
    ├── app
    │   ├── __init__.py
    │   ├── config.py       # настройки (URL БД, ES, имя индекса)
    │   ├── database.py     # подключение к PostgreSQL (async engine, session)
    │   ├── models.py       # SQLAlchemy-модель Document
    │   ├── schemas.py      # Pydantic-схемы запроса/ответа
    │   ├── search.py       # работа с Elasticsearch (индекс, поиск, удаление)
    │   ├── service.py      # связка ES + PostgreSQL
    │   ├── seed.py         # скрипт загрузки CSV в БД и ES
    │   └── main.py         # FastAPI-приложение и эндпоинты
    ├── data
    │   └── posts.csv       # исходные данные
    ├── tests
    │   ├── __init__.py
    │   └── test_api.py     # тесты
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── pytest.ini
    ├── docs.json        
    └── README.md


## Требования

- Docker
- Python 3.12
- Файл `posts.csv` внутри репозитория

## Запуск

```bash
cd doc-search
docker compose up -d --build
```
Доступ к сервису:
 
- Swagger UI: http://localhost:8000/docs
- OpenAPI: http://localhost:8000/openapi.json


Остановка:
 
```bash
docker compose down        # остановить, данные сохранятся
docker compose down -v     # остановить и удалить данные
```

## Примеры запросов
 
Поиск:
 
```bash
curl -G "http://localhost:8000/search" --data-urlencode "q={машины}"
```
 
Удаление:
 
```bash
curl -X DELETE http://localhost:8000/documents/1
```
 
## Тестирование

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

