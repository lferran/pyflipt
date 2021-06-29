from aiohttp import ClientSession

from pyflipt import models

__all__ = ["get_client", "FliptClient", "FliptError"]


def safe_path_join(*url_parts) -> str:
    parts = []
    n_parts = len(url_parts)
    for index, part in enumerate(url_parts):
        if index == 0:
            parts.append(part.rstrip("/"))
        elif index == n_parts - 1:
            parts.append(part.lstrip("/"))
        else:
            parts.append(part.rstrip("/").lstrip("/"))
    return "/".join(parts)


CONFLICT_CODE = 3


class FliptError(Exception):
    def __init__(self, resp_json):
        self.resp_json = resp_json

    def __repr__(self):
        return f"FliptError({self.resp_json})"


class FliptClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self._session = ClientSession()

    async def create(self, unit: models.FliptBasicUnit):
        if isinstance(unit, models.Flag):
            url = safe_path_join(self.base_url, "/flags")
        elif isinstance(unit, models.Segment):
            url = safe_path_join(self.base_url, "/segments")
        elif isinstance(unit, models.Constraint):
            url = safe_path_join(
                self.base_url, f"/segments/{unit.segment_key}/constraints"
            )
        elif isinstance(unit, models.Rule):
            url = safe_path_join(self.base_url, f"/flags/{unit.flag_key}/rules")
        else:
            raise ValueError(f"Not supported yet {unit}")

        async with self._session.post(url, data=unit.json()) as resp:
            if resp.status == 200:
                return
            resp_json = await resp.json()
            if resp.status == 400:
                if resp_json.get("code") == CONFLICT_CODE:
                    # Already there
                    return
            raise FliptError(resp_json)

    async def close(self):
        if not self._session.closed:
            await self._session.close()


def get_client(base_url) -> FliptClient:
    return FliptClient(base_url)
