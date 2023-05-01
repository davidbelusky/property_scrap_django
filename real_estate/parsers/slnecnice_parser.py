import asyncio
import math

import requests
from aiohttp.client import ClientSession
from real_estate.parsers.parser import Parser


class SlnecniceParser(Parser):
    KEY_IDENTIFICATOR = "data"

    def __init__(self):
        self.source = "slnecnice"
        self.url = "https://api.slnecnice.sk/api/flats?page={}&status[]=P&status[]=Y"
        self.keys = [
            "id",
            "status_name",
            "type_name",
            "rooms",
            "floor",
            "area",
            "area_total",
            "price",
        ]
        self.mapped_keys = list(zip(self.keys, Parser.DEFAULT_KEYS))
        self.headers = {"Content-type": "application/json"}
        self.data = []

    def get_init_data_and_tasks(self, session: ClientSession) -> tuple:
        response = requests.get(self.url.format(1), headers=self.headers)
        self.data = self.data + response.json()["data"]
        number_of_pages = math.ceil(response.json()["count"] / Parser.PAGE_SIZE) - 1
        tasks = self._get_tasks(session, number_of_pages)
        return self.data, tasks

    def _get_tasks(self, session: ClientSession, number_of_pages: int) -> list:
        tasks = []
        for page in range(2, number_of_pages):
            tasks.append(
                asyncio.create_task(
                    session.get(self.url.format(page), headers=self.headers, ssl=False)
                )
            )
        return tasks

    def parse_data(self, data: list) -> list:
        parsed_data = []
        for property in data:
            new_dict = {"source": self.source}
            for key in self.mapped_keys:
                if key[0] == "status_name":
                    property[key[0]] = True if property[key[0]] == "voľná" else False
                new_dict[key[1]] = property[key[0]]
            parsed_data.append(new_dict)
        return parsed_data
