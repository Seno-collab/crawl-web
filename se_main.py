import csv
import re
import time
from typing import List
from selenium import webdriver
from selenium.webdriver.common.by import By
from icecream import ic  # type: ignore


def find_all_tag(value: str):
    return re.findall(r"<p>.*?</p>", value)


list_5: List[dict[str, str]] = []

driver = webdriver.Edge()
i = 1
while True:
    if i > 39:
        break
    dic_5: dict[str, str] = {}
    url = f"https://www.manythings.org/voa/words/{i}.html"
    ic(url)
    driver.get(url)
    dic_5["title"] = driver.title
    elements = driver.find_elements(By.TAG_NAME, "p")
    dic_5["content"] = ""
    for index, element in enumerate(elements):
        if len(elements) - 1 == index or index == 0:
            dic_5["content"] += element.text
        else:
            dic_5["content"] += element.text + "\n"
    audio_link = driver.find_element(By.TAG_NAME, "source")
    dic_5["audio_link"] = audio_link.get_attribute("src")
    sources = driver.find_elements(By.TAG_NAME, "small")
    for source in sources:
        if source.text.startswith("www"):
            dic_5["additional_information"] = source.text
        if source.text.startswith("Source:"):
            match = re.search(r"Source:.*", source.text)
            dic_5["source"] = match.group().replace("Source:", "")
    dic_5["listening_duration"] = "5"
    list_5.append(dic_5)
    i += 1
driver.quit()
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
    for entry in list_5:
        w.writerow(entry)
