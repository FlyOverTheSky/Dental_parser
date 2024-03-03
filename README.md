# Dental Parser
Сервис парсинга цен для закупок стоматологий

## Технологии
- Python
- Fastapi
- Selenium
- Redis

## Использование
Установить и запустить redis-сервер для кэширования

Запустить fastapi-сервер (в инструкции пример на uvicorn):


```
git clone git@github.com:FlyOverTheSky/Dental_parser.git
```

```
python -m venv venv

sourve venv/Scripts/activate

pip install -r requirements.txt

uvicorn app:app
```

### Документация
- /swagger
- /redoc

### Выполненые задачи
- Настроен парсер для сайта Пробахилы
- Настроен парсер для сайта Averon
- Создано интерфейс на Fastapi
- Подключен redis для кэширования результатов
