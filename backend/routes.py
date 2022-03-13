from flask import Blueprint, request

routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/")
def test():
    return "Home page!!!!"


from flask import Blueprint
import requests
from bs4 import BeautifulSoup


@routes_bp.route("/crypto-data", methods=["POST", "OPTIONS"])
def get_crypto_data():
    print("TEST")


@routes_bp.route("/get-crypto-news")
def crypto_news_aggregator():
    test = get_news_from_crypto_news()
    return test


def get_news_from_crypto_news():
    # gettings crypto news from cryptonews.com
    URL = "https://cryptonews.com/"
    page = requests.get(URL)
    crypto_soup = BeautifulSoup(page.content, "html.parser")
    news_title_element = crypto_soup.find_all(
        "a", class_="article__title article__title--lg article__title--featured  mb-20"
    )
    for news_title in news_title_element:
        print(news_title, end="\n", flush=True)
    return news_title_element
