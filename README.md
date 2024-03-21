# Dental Parser
Сервис парсинга цен для закупок стоматологий

## Технологии
- Python
- Fastapi
- Selenium
- Redis

## Использование
```
git clone git@github.com:FlyOverTheSky/Dental_parser.git
```

```
docker compose up
```

### Документация
- /parse | request body: (string)item_name - наименование для поиска, (int)count_to_search - количество результатов
- /swagger
- /redoc

### Выполненые задачи
- Настроен парсер для сайта Пробахилы
- Настроен парсер для сайта Averon
- Создан интерфейс на Fastapi
- Подключен redis для кэширования результатов
- Настроены контейнеры
- Написан docker-compose
