from abc import abstractmethod

from aiohttp.client import ClientSession


class Parser:
    DEFAULT_KEYS = [
        "source_id",
        "available",
        "apartment_type",
        "rooms",
        "floor",
        "area_size",
        "area_total_size",
        "price",
    ]
    PAGE_SIZE = 15
    KEY_IDENTIFICATOR = ""

    def __init__(self):
        self.source = ""
        self.url = ""
        self.keys = []
        self.mapped_keys = list(zip(self.keys, Parser.DEFAULT_KEYS))
        self.headers = {}
        self.data = []

    @abstractmethod
    def get_init_data_and_tasks(self, session: ClientSession) -> tuple:
        """Get first page data and generate async tasks for all remaining pages"""
        pass

    @abstractmethod
    def _get_tasks(self, session: ClientSession, number_of_pages: int) -> list:
        """Generate async task for each page and return list of tasks"""
        pass

    @abstractmethod
    def parse_data(self, data: list) -> list:
        """Parse and clean downloaded data"""
        pass
