from fastapi import FastAPI
from pydantic import BaseModel

from parsers.probahily import ProbahilyParser
from parsers.averon import AveronParser

app = FastAPI()
parsers_lits = []

probahily_parser = ProbahilyParser()
parsers_lits.append(probahily_parser)

averon_parser = AveronParser()
parsers_lits.append(averon_parser)


class ParseRequest(BaseModel):
    item_name: str
    count_to_search: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/parse/")
async def parse_item(parse_request: ParseRequest):
    search_results = {}
    for parser in parsers_lits:
        parser.parse_names_and_prices(
            to_search=parse_request.item_name,
            return_items_count=parse_request.count_to_search
        )
        search_results[parser.company_name] = parser.last_results
    return search_results
