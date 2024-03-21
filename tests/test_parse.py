import requests

from tests.api import Parsing
from tests.models import ParsingItem


class TestParsing:
    def test_parsing_gloves(self):
        parse_gloves = ParsingItem(item_name="Перчатки", count_to_search=10)
        parsing_object = Parsing()
        body = parse_gloves.get_data()
        print(parsing_object)
        print(body)
        response = parsing_object.parsing_item(body=body)
        assert response.status_code == 200


if __name__ == "__main__":
    # TestParsing().test_parsing_gloves()
    request = requests.get(
        url="http://0.0.0.0:8000/parse/",
        json={
    "item_name": "Перчатки",
    "count_to_search": 10
}
    )
    print(request.status_code)
