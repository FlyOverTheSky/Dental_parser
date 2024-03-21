import asyncio

from backend.parsers.averon import AveronParser
from backend.parsers.probahily import ProbahilyParser

parsers_list = []

probahily_parser = ProbahilyParser()
parsers_list.append(probahily_parser)

averon_parser = AveronParser()
parsers_list.append(averon_parser)
# async def test_parsing(name, count):
#     loop_for_parsers = asyncio.get_event_loop()
#     parsers_tasks_list = []
#     # try:
#     for parser in parsers_list:
#         loop_for_parsers.create_task(
#             parser.parse_names_and_prices(
#                 to_search=name,
#                 return_items_count=count
#             )
#         )
#     search_results = [parser.last_results for parser in parsers_list]
#     # finally:
#     #     loop_for_parsers.close()
#
#     return search_results


async def test_parsing(name, count):
    loop_for_parsers = asyncio.get_running_loop()
    parsers_tasks_list = []
    for parser in parsers_list:
        task= loop_for_parsers.create_task(
            parser.parse_names_and_prices(
                to_search=name,
                return_items_count=count
            )
        )
        parsers_tasks_list.append(task)
    search_results = {}
    while parsers_tasks_list:
        current_task = parsers_tasks_list[-1]
        print(current_task)
        await current_task
        if current_task.done():
            search_results = {**search_results, **current_task.result()}
            parsers_tasks_list.pop()
    else:
        return search_results



async def main():
    name = "Иглы"
    count = 2
    print(await test_parsing(name, count))

asyncio.run(main())
