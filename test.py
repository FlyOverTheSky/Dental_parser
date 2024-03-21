from backend.parsers.probahily import ProbahilyParser


parser = ProbahilyParser()
parser.parse_names_and_prices(
    to_search="Перчатки",
    return_items_count=10
)
print(parser.last_results)