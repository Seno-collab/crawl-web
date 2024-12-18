import csv
import json
from icecream import ic  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import requests  # type: ignore
import re
import unicodedata
from typing import List, Dict

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
}


def remove_special_characters(value: str) -> str:
    modified_text = unicodedata.normalize("NFKC", value)
    return modified_text


def replace_space_string(value: str) -> str:
    value = remove_special_characters(value)
    modified_text = re.sub(r"(\b\w+)\.(\w+\b)", r"\1.\t\2", value)
    return modified_text


list_15: List[Dict[str, str]] = []
urls = [
    "https://www.manythings.org/voa/stories/",
    "https://www.manythings.org/voa/history/",
]
for url in urls:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    h3s = soup.find_all("h3")
    links_with_text = []
    for a in soup.find_all("a", href=True):
        dic_15: dict[str, str] = {}
        if a.text:
            endpoint = a.get("href")
            # skip url http
            if endpoint.startswith("http") is False:
                url_children = f"{url}{endpoint}"
                ic(url_children, endpoint)
                page__child = requests.get(url_children, headers=headers)
                soup = BeautifulSoup(page__child.content, "html.parser")
                contents = soup.find_all("p")
                dic_15["content"] = ""
                for index, content in enumerate(contents):
                    if len(contents) - 1 == index or index == 0:
                        dic_15["content"] += remove_special_characters(content.text)
                    else:
                        dic_15["content"] += (
                            remove_special_characters(content.text) + "\n"
                        )
                if soup.find("h1") is None:
                    dic_15["title"] = soup.find("h2").text.strip()
                else:
                    dic_15["title"] = soup.find("h1").text.strip()
                dic_15["listening_duration"] = "15"
                smalls = soup.find_all("small")
                for small in smalls:
                    s = small.text.strip()
                    if s.startswith("www"):
                        dic_15["additional_information"] = s
                    if s.startswith("Source:"):
                        match = re.search(r"Source:.*?=", s)
                        dic_15["source"] = (
                            match.group()
                            .rstrip("=")
                            .strip()
                            .replace("Source:", "")
                            .replace("TEXT", "")
                        )
                        ic(dic_15["source"])
                for script in soup.find_all("script"):
                    text = script.string
                    if text is not None and text.startswith("MP3"):
                        dic_15["audio_link"] = (
                            text.replace(";", "")
                            .replace('MP3Player("', "")
                            .replace('"', "")
                            .replace(")", "")
                            .replace(",", "")
                            .replace("'", "")
                        )
                list_15.append(dic_15)
with open("data_15.csv", "w", newline="") as f:
    w = csv.DictWriter(
        f,
        [
            "title",
            "audio_link",
            "source",
            "content",
            "listening_duration",
            "additional_information",
        ],
    )
    w.writeheader()
    for entry_15 in list_15:
        w.writerow(entry_15)
list_5: List[dict[str, str]] = []
i = 1
while True:
    dic_5: dict[str, str] = {}
    url = f"https://www.manythings.org/voa/words/{i}.html"
    ic(url)
    page = requests.get(url, headers=headers)
    if page.status_code != 200 or i > 39:
        ic(i)
        break
    soup = BeautifulSoup(page.content, "html.parser")
    contents = soup.find_all("p")
    dic_5["content"] = ""
    for index, content in enumerate(contents):
        if len(contents) - 1 == index or index == 0:
            dic_5["content"] += remove_special_characters(content.text)
        else:
            dic_5["content"] += remove_special_characters(content.text) + "\n"
    ic(dic_5["content"])
    dic_5["title"] = soup.find("title").text.strip().replace(",", "")
    ic(dic_5["title"])
    dic_5["listening_duration"] = "5"
    smalls = soup.find_all("small")
    for small in smalls:
        s = small.text.strip()
        if s.startswith("www"):
            dic_5["additional_information"] = s
            ic(dic_5["additional_information"])
        if s.startswith("Source:"):
            match = re.search(r"Source:.*?=", s)
            dic_5["source"] = match.group().rstrip("=").strip().replace("Source:", "")
            ic(dic_5["source"])
    for script in soup.find_all("script"):
        text = script.string
        if text is not None and text.startswith("MP3"):
            dic_5["audio_link"] = (
                text.replace(";", "")
                .replace('MP3Player("', "")
                .replace('"', "")
                .replace(")", "")
                .replace(",", "")
            )
    list_5.append(dic_5)
    break
    i += 1
with open("data_5.csv", "w", newline="") as f:
    w = csv.DictWriter(
        f,
        [
            "title",
            "audio_link",
            "source",
            "content",
            "listening_duration",
            "additional_information",
        ],
    )
    w.writeheader()
    ic(list)
    for entry in list_5:
        w.writerow(entry)
