from time import time
from tracemalloc import start
from flask import Blueprint, request
from flask_cors import cross_origin
from controllers import start_analyser_process, crypto_getter_blockchair

crypto_processes = Blueprint('crypto_processes', __name__)


@crypto_processes.route('/api/analyser-input', methods=["POST", "OPTIONS"])
@cross_origin()
def start_analyser():
    try:
        analyser_input = request.get_json()
    except:
        return "Invalid request please try again", 401

    crypto_name = analyser_input["crypto_name"]
    time_range = analyser_input["time_range"]
    print(f"{crypto_name}-{time_range}", flush="true")
    return start_analyser_process(crypto_name, time_range)
    # return crypto_getter_blockchair(crypto_name, ['bitcoin'])


@crypto_processes.route('/api/market-indicator')
def market_indicator():
    try:
        analyser_input = request.get_json()
    except:
        return "Invalid request please try again", 401

    crypto_name = analyser_input["crypto_name"]
    time_range = analyser_input["time_range"]
    print(f"{crypto_name}-{time_range}", flush="true")
    return start_analyser_process(crypto_name, time_range)


@crypto_processes.route('/api/twitter-opinion-leaders')
def twitter_opinion_leaders():
    pass


@crypto_processes.route('/api/reddit-top-servers')
def reddit_top_servers():
    pass


@crypto_processes.route('/api/crypto-outlet-news')
def crypto_outlet_news():
    pass
