import time
from urllib.parse import urljoin
import csv
from bs4 import BeautifulSoup
import httpx
import requests

import asyncio


from dataclasses import dataclass

URL = "https://djinni.co/jobs/?primary_keyword=Python"


def get_num_pages(client: httpx.Client = httpx.Client(), url: str = URL) -> int:
    response = client.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    pagination = soup.select_one(".pagination_with_numbers")

    if pagination is None:
        return 1

    return int(pagination.select("li")[-3].text)


if __name__ == '__main__':
    print(get_num_pages())
