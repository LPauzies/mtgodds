import asyncio
import gzip
import shutil
from typing import Any

import httpx

from config import APP, VERSION

class ScryfallAPIClient(httpx.AsyncClient):
    BASE_URL: str = "https://api.scryfall.com"

    def _request_headers(self):
        return {
            "User-Agent": f"{APP}/{VERSION}",
            "Accept": "application/json",
        }

    async def get_bulk_data_default_cards_jsonl(self) -> dict[str, Any]:
        response = await self.get(f"{self.BASE_URL}/bulk-data/default-cards", headers=self._request_headers())
        return response.json()

    async def get_bulk_data_oracle_tags_jsonl(self) -> dict[str, Any]:
        response = await self.get(f"{self.BASE_URL}/bulk-data/oracle-tags", headers=self._request_headers())
        return response.json()

    async def download_bulk(self, bulk_data: dict[str, Any]) -> str:
        download_uri = bulk_data["jsonl_download_uri"]
        bulk_type = bulk_data["type"]
        response = await self.get(download_uri)

        archive_path = f"/tmp/{bulk_type}.jsonl.gz"
        data_path = f"/tmp/{bulk_type}.jsonl"
        with open(archive_path, "wb") as fp:
            fp.write(response.content)

        with gzip.open(archive_path, "rb") as descriptor_archive:
            with open(data_path, "wb") as descriptor_jsonl:
                shutil.copyfileobj(descriptor_archive, descriptor_jsonl)

        return data_path



if __name__ == '__main__':
    async def main():
        async with ScryfallAPIClient() as client:
            value = await client.get_bulk_data_default_cards_jsonl()
            print(value)
            value = await client.download_bulk(value)
            print(value)
            value = await client.get_bulk_data_oracle_tags_jsonl()
            print(value)
            value = await client.download_bulk(value)
            print(value)

    asyncio.run(main())
