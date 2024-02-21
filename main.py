from pprint import pprint

from parsers.probahily import ProbahilyParser
from parsers.averon import AveronParser


if __name__ == '__main__':
    names_to_search = input('Что найти?')
    counts_to_search = int(input('Сколько результатов вернуть?'))
    # averon_parser = AveronParser()
    # averon_parser.parse_names_and_prices(
    #     to_search=names_to_search,
    #     return_items_count=counts_to_search
    # )
    # pprint(averon_parser.last_results)

    probahily_parser = ProbahilyParser()
    probahily_parser.parse_names_and_prices(
        to_search=names_to_search,
        return_items_count=counts_to_search
    )
    pprint(probahily_parser.last_results)


    # if isinstance(results_probahily, str):
    #     print(results_probahily)
    # else:
    #     for item, price in results_probahily:
    #         print(f"Наименование: {item}. Цена: {price}")
