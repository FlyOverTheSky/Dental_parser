from faker import Faker

fake = Faker()


class ParsingItem:
    def __init__(self, item_name: str, count_to_search: int):
        self.item_name = item_name
        self.count_to_search = count_to_search

    def get_data(self):
        data = {
            "item_name": self.item_name,
            "count_to_search": self.count_to_search,
        }
        return data
