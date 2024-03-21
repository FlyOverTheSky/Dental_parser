import requests
from jsonschema import validate

from backend.settings import API_URL


class Parsing:
    def __init__(self):
        self.url = API_URL + "parse/"

    def __str__(self):
        return self.url

    def parsing_item(self, body: dict):
        # , schema: dict
        response = requests.get(self.url, json=body)
        # validate(instance=response.json(), schema=schema)
        return response
