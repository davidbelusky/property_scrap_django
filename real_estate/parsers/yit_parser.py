import asyncio
import copy
import json
import math

import requests
from aiohttp.client import ClientSession
from real_estate.parsers.parser import Parser

APARTMENTS_REQUEST_BODY = {
    "PageSize": Parser.PAGE_SIZE,
    "StartPage": 1,
    "QueryString": "*",
    "UILanguage": "sk",
    "PageId": 21747,
    "BlockId": 0,
    "SiteId": "yit.sk",
    "Attrs": ["inap"],
    "Fields": None,
    "CacheMaxAge": 0,
    "Filter": {
        "Field": "Locale",
        "Value": "sk",
        "Operator": "Equals",
        "AndConditions": [
            {
                "Field": "ProjectPublish",
                "Value": True,
                "Operator": "Equals",
                "AndConditions": [],
                "OrConditions": [],
            },
            {
                "Field": "IsAvailable",
                "Value": True,
                "Operator": "Equals",
                "AndConditions": [],
                "OrConditions": [],
            },
            {
                "Field": "ProductItemForSale",
                "Value": True,
                "Operator": "Equals",
                "AndConditions": [],
                "OrConditions": [],
            },
            {
                "Field": "AreaIds",
                "Value": "cityv62u-q27j-49ue-j59q86mus34t",
                "Operator": "Any",
                "AndConditions": [],
                "OrConditions": [],
            },
            {
                "Field": "BuildingTypeKey",
                "Value": ["BlockOfFlats", "SemiDetachedHouse", "DetachedHouse"],
                "Operator": "In",
                "AndConditions": [],
                "OrConditions": [],
            },
        ],
        "OrConditions": [],
    },
    "Facet": [],
    "Order": [{"Field": "ReservationStatusIndex"}, {"Field": "CrmId"}],
}


class YitParser(Parser):
    KEY_IDENTIFICATOR = "Hits"

    def __init__(self):
        self.source = "yit"
        self.url = "https://www.yit.sk/api/v1/productsearch/apartments"
        self.keys = [
            "ApartmentId",
            "ReservationStatus",
            "ApartmentType",
            "NumberOfRooms",
            "FloorNumber",
            "ApartmentSize",
            "TotalAreaSize",
            "SalesPrice",
        ]
        self.mapped_keys = list(zip(self.keys, Parser.DEFAULT_KEYS))
        self.headers = {"Content-type": "application/json"}
        self.data = []

    def get_init_data_and_tasks(self, session: ClientSession) -> tuple:
        response = requests.post(
            self.url, data=json.dumps(APARTMENTS_REQUEST_BODY), headers=self.headers
        )
        number_of_pages = math.ceil(response.json()["TotalHits"] / Parser.PAGE_SIZE) - 1
        self.data = self.data + response.json()["Hits"]
        tasks = self._get_tasks(session, number_of_pages)
        return self.data, tasks

    def _get_tasks(self, session: ClientSession, number_of_pages: int) -> list:
        tasks = []
        for page in range(2, number_of_pages):
            input_body = copy.deepcopy(APARTMENTS_REQUEST_BODY)
            input_body["StartPage"] = page
            tasks.append(
                asyncio.create_task(
                    session.post(
                        self.url,
                        data=json.dumps(input_body),
                        headers=self.headers,
                        ssl=False,
                    )
                )
            )
        return tasks

    def parse_data(self, data: list) -> list:
        parsed_data = []
        for hit in data:
            fields = hit["Fields"]
            new_dict = {"source": self.source}
            for key in self.mapped_keys:
                if key[0] == "ReservationStatus":
                    fields[key[0]] = True if fields[key[0]] == "Voľný" else False
                new_dict[key[1]] = fields[key[0]]
            parsed_data.append(new_dict)
        return parsed_data
