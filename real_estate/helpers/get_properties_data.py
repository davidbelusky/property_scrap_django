import asyncio

import aiohttp
from django.conf import settings
from real_estate.parsers.slnecnice_parser import SlnecniceParser
from real_estate.parsers.yit_parser import YitParser


async def get_properties_data_async() -> dict:
    """Asynchronously download properties data and return in format {"parser_source": [list of properties]}"""
    raw_results = []
    all_tasks = []
    result = {parser().source: [] for parser in settings.PARSERS}

    async with aiohttp.ClientSession() as session:
        for parser in settings.PARSERS:
            data, tasks = parser().get_init_data_and_tasks(session)
            result[parser().source] += data
            all_tasks += tasks

        responses = await asyncio.gather(*all_tasks)
        for response in responses:
            raw_results.append(await response.json())

        for raw_result in raw_results:
            if SlnecniceParser.KEY_IDENTIFICATOR in raw_result:
                result[SlnecniceParser().source] += raw_result[
                    SlnecniceParser.KEY_IDENTIFICATOR
                ]
            if YitParser.KEY_IDENTIFICATOR in raw_result:
                result[YitParser().source] += raw_result[YitParser.KEY_IDENTIFICATOR]

        return result
