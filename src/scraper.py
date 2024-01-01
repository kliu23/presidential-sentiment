from typing import Optional
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


logger = logging.getLogger(__name__)
driver = webdriver.Safari()


def selenium_helper_scroll_down(percent: float) -> None:
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight*{percent});")
    time.sleep(3)


def selenium_helper_infinite_scroll() -> None:
    last_scrolled_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        selenium_helper_scroll_down(1.0)

        new_scrolled_height = driver.execute_script("return document.body.scrollHeight")
        if new_scrolled_height == last_scrolled_height:
            break
        last_scrolled_height = new_scrolled_height



def get_speech_links(url: str) -> dict:
    speeches = {
        "speeches": [],
    }

    driver.get(url)
    time.sleep(3)

    selenium_helper_infinite_scroll()

    links = driver.find_elements(By.XPATH, "//a[contains(@href, 'presidential-speeches')]")
    speech_links = [link.get_attribute("href") for link in links]
    
    speeches["speeches"] = speech_links

    return speeches


def get_speech_text() -> dict:
    with open('speeches.json') as f:
        speeches = json.load(f)
    
    speech_text = {

    }

    for speech in speeches["speeches"]:
        driver.get(speech)
        time.sleep(1.5)

        text = driver.find_element(By.XPATH, "//div[@class='view-transcript']").text
        title = driver.find_element(By.XPATH, "//title").text
        name = driver.find_element(By.XPATH, "//p[@class='president-name']").text
        try:
            date = driver.find_element(By.XPATH, "//p[@class='episode-date']").text
        except:
            date = ""

        try:
            location = driver.find_element(By.XPATH, "//span[@class='speech-loc']").text
        except:
            location = ""

        try:
            intro = driver.find_element(By.XPATH, "//div[@class='about-sidebar--intro']").text
        except:
            intro = ""

        if name not in speech_text:
            speech_text[name] = []

        speech_text[name].append({
            "title": title,
            "date": date,
            "location": location,
            "intro": intro,
            "transcript": text,
        })

        print(f"Finished {title}")
    
    return speech_text
        


if __name__ == "__main__":
    # url = "https://millercenter.org/the-presidency/presidential-speeches"
   
    speech_text = get_speech_text()
    
    with open('webscrape-results/speech_text_by_president.json', 'w') as f:
        json.dump(speech_text, f, indent=4)