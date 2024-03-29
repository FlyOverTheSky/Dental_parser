import asyncio
import json
from fastapi import FastAPI
from pydantic import BaseModel
import redis.asyncio as redis

from parsers.probahily import ProbahilyParser
from parsers.averon import AveronParser
from settings import *

app = FastAPI()
parsers_list = []

probahily_parser = ProbahilyParser()
parsers_list.append(probahily_parser)

averon_parser = AveronParser()
parsers_list.append(averon_parser)


class ParseRequest(BaseModel):
    item_name: str
    count_to_search: int


async def get_cached_items(
        redis_connection,
        item_name: str,
        items_count: int,
        company_name: str):
    """Метод для проверки есть ли эти данные в кэше."""
    # TODO: Проверка в кэше по компании и количеству закэшированных резульатов.
    cached_results = await redis_connection.get(item_name)
    if not cached_results:
        return None
    return json.loads(cached_results)


@app.get("/parse/")
async def parse_item(parse_request: ParseRequest):
    """Парсинг по наименованию."""
    search_results = {}

    redis_connection = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    )
    cache_key = parse_request.item_name

    loop_for_parsers = asyncio.get_running_loop()
    for parser in parsers_list:
        # TODO: Переводить имя на англ для удобства проверки redis
        print(parser.company_name, "start parser")
        cached_results = await get_cached_items(
            redis_connection=redis_connection,
            item_name=cache_key,
            items_count=parse_request.count_to_search,
            company_name=parser.company_name
        )
        # Если в кэше есть нужные наименования
        if cached_results:
            print(parser.company_name, "find in cached")
            search_results = {**search_results, **cached_results}
            cached_results = {}
            continue
        print(parser.company_name, "not found in cached")
        # Если в кэше нет данных, то запускаем парсер.
        print(parser.company_name, "generate task")
        task = loop_for_parsers.create_task(
            parser.parse_names_and_prices(
                to_search=parse_request.item_name,
                return_items_count=parse_request.count_to_search
            )
        )
        await task
        search_results = {**search_results, **task.result()}

        # Кэшируем результаты поиска
        # await redis_connection.setex(
        #     name=cache_key,
        #     value=json.dumps(search_results),
        #     time=CACHE_TIME_LIMIT,
        # )
    return search_results
