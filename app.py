from fastapi import FastAPI
from pydantic import BaseModel
import redis.asyncio as redis
import json
from googletrans import Translator

from parsers.probahily import ProbahilyParser
from parsers.averon import AveronParser

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
    cached_results = await redis_connection.get(item_name)
    if not cached_results:
        return None
    return json.loads(cached_results)


@app.get("/parse/")
async def parse_item(parse_request: ParseRequest):
    search_results = {}

    redis_connection = redis.Redis(
        host='127.0.0.1',
        port=6379,
    )
    cache_key = parse_request.item_name

    for parser in parsers_list:
        # Переводить имя на англ для удобства проверки redis
        cached_results = await get_cached_items(
            redis_connection=redis_connection,
            item_name=cache_key,
            items_count=parse_request.count_to_search,
            company_name=parser.company_name
        )

        if cached_results:
            search_results[parser.company_name] = parser.last_results
            continue

        parser.parse_names_and_prices(
            to_search=parse_request.item_name,
            return_items_count=parse_request.count_to_search
        )
        search_results[parser.company_name] = parser.last_results

    await redis_connection.setex(
        name=cache_key,
        value=json.dumps(search_results),
        time=30,
    )

    return search_results
