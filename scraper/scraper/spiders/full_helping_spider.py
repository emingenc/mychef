import scrapy
import requests

from bs4 import BeautifulSoup


class UrlExtractor:
    """Utility for extracting the start url for the spider"""
    def __init__(self, url):
        self.url = url
        self.content = self.get_start_page()

    def get_start_page(self):
        try:
            return requests.get(self.url).content
        except requests.exceptions.ConnectionError as e:
            raise(e)

    def get_recipe_url(self):
        soup = BeautifulSoup(self.content, "html.parser")
        latest_post = soup.find("div", {"class": "single-posty"})
        start_url = latest_post.find("a")["href"]
        return [start_url]


class FullHelpingSpider(scrapy.Spider):
    """Scrape the website thefullhelping.com and post results to mychef"""
    name = "full_helping"
    download_delay = 8
    sid = 1

    def __init__(self, page=1):
        self.url = f"https://www.thefullhelping.com/recipe-index/?sf_paged={page}"
        self.start_urls = UrlExtractor(self.url).get_recipe_url()

    def parse(self, response):
        if response.css(".wprm-recipe-ingredients-container"):
            payload = {
                "name": response.css(".title::text").get(),
                "url": response.url,
                "image": self.get_image_url(response),
            }
            requests.post(f"http://api:8000/sources/{self.sid}/recipes/", json=payload)

        for a in response.css(".nav-previous a"):
            yield response.follow(a, callback=self.parse)

    def get_image_url(self, response):
        img = response.css("p > img")
        return img.re_first(r'src="(http.*?)\"')

    def get_ingredients(self, response):
        pass
