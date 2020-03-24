import os
import string

import scrapy
import requests

from bs4 import BeautifulSoup


def get_latest_recipe():
    """Extract first url from recipe index on fullhelping webpage"""
    index_url = "https://www.thefullhelping.com/recipe-index/"
    res = requests.get(index_url)
    soup = BeautifulSoup(res.content)
    start_url = soup.find("div", {"class": "single-posty"}).find("a")["href"]
    return [start_url]


class FullHelpingSpider(scrapy.Spider):
    """Scrapes the website <thefullhelping.com> and posts to mychef"""

    name = "full_helping"
    sid = 1
    download_delay = 8
    start_urls = get_latest_recipe()

    def parse(self, response):
        if response.css(".wprm-recipe-ingredients-container"):
            payload = {
                "name": response.css(".title::text").get(),
                "url": response.url,
                "image": self.get_image_url(response),
            }
            requests.post(f"http://api:8000/sources/{self.sid}/recipes/", json=payload)

        next_page_link = response.css(".nav-previous a::attr(href)").get()
        if next_page_link:
            next_page = response.urljoin(next_page_link)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def get_image_url(self, response):
        img = response.css("p > img")
        return img.re_first(r'src="(http.*?)\"')

    def get_ingredients(self, response):
        pass
