from aiohttp import ClientSession
from .models import FliptBasicUnit


__all__ = ["get_client", "get_session"]


class FliptSession(ClientSession):
    pass


class FliptClient:
    def __init__(self):
        self.session = get_session()

    async def create(unit: FliptBasicUnit):
        pass


def get_client() -> FliptClient:
    return FliptClient()


def get_session():
    return FliptSession()
