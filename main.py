from parsers.probahily_rf import parse_names_and_prices

if __name__ == '__main__':
    names_to_search = input('Что найти?')
    counts_to_search = int(input('Сколько результатов вернуть?'))
    results = parse_names_and_prices(
        to_search=names_to_search,
        return_items_count=counts_to_search
    )
    if isinstance(results, str):
        print(results)
    else:
        for item, price in results:
            print(f"Наименование: {item}. Цена: {price}")
