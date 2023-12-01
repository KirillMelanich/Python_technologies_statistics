import time
from urllib.parse import urljoin
import csv
from bs4 import BeautifulSoup
import httpx
import requests

import asyncio


from dataclasses import dataclass

URL = "https://djinni.co/jobs/?primary_keyword=Python"


def get_num_pages(url: str = URL) -> int:
    response = httpx.Client().get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    pagination = soup.select_one(".pagination_with_numbers")

    if pagination is None:
        return 1

    return int(pagination.select("li")[-3].text)


def get_num_jobs(url: str = URL):
    response = httpx.Client().get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    num_jobs = soup.select_one(".text-muted").text

    return int(num_jobs)


def get_clean_description(vacancy_soup: BeautifulSoup):
    description_element = vacancy_soup.select_one(".job-list-item__description > span")
    description = (
        description_element.get("data-original-text", "").strip().rstrip().lower()
    )
    description = BeautifulSoup(description, "html.parser").get_text()
    return description


def parse_single_page_jobs(page: int, client: httpx.Client = httpx.Client(), url: str = URL):
    response = client.get(url, params={"page": page})
    soup = BeautifulSoup(response.content, "html.parser")

    job_descriptions = []
    for job in soup.findAll("div", class_="job-list-item__description"):
        job_descriptions.append(get_clean_description(job))

    return job_descriptions


def parse_first_page_jobs(client: httpx.Client = httpx.Client(), url: str = URL):
    response = client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    job_descriptions = []
    for job in soup.findAll("div", class_="job-list-item__description"):
        job_descriptions.append(get_clean_description(job))

    return job_descriptions


def parse_all_pages():
    with httpx.Client() as client:
        all_jobs_descriptions = [parse_first_page_jobs(client, URL)]
        for page in range(2, get_num_pages() + 1):
            one_page = parse_single_page_jobs(page, client, URL)
            all_jobs_descriptions.append(one_page)

    return all_jobs_descriptions


def main() -> None:
    for i in parse_all_pages():
        print(i)


if __name__ == '__main__':
    start = time.perf_counter()
    num_pages = get_num_pages()
    print(f"Number of pages is {num_pages}")
    print(f"Number of jobs is {get_num_jobs()}")
    main()
    duration = time.perf_counter() - start
    print(f"program runs in {duration} seconds")