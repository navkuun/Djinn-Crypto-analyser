import requests  # used for http requests e.g. GET, POST, PUT etc...
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
# imports
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from dateutil import parser
from datetime import datetime, timedelta
from datetime import date
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import twitter_samples
import string
from os import getcwd
from collections import defaultdict
import json
nltk.download('twitter_samples')
nltk.download('stopwords')
# used for vader sentiment analysis
nltk.download('vader_lexicon')

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>')

# vader new sords to add relating to crypto, +4 = most postitve, -4 = most negative
new_words = {
    "hodl": 3.4,
    "pump": 2.0,
    "dump": -3.0,
    "bear": -1.0,
    "bearish": -2.0,
    "bullish": 2.5,
    "bull": 1.5,
    "dip": 1.0,
    "wall": -1.0,
    "buy": 3.0,
    "sell": -3.0
}

# CRYPTOCURRENCY GETTERS


class get_crypto_stats:
    # constructor
    def __init__(self, cryptoName: str, availableCryptocurrencies: list):
        self.crypto_name = cryptoName  # name of cryptocurrency passed by user
        self.available_cryptocurrencies = availableCryptocurrencies
        # the available list of cryptocurrencies
    # this methods gets the cryptocurrency data

    def blockchair(self):
        if(self.crypto_name in self.available_cryptocurrencies):
            url = f"https://api.blockchair.com/{self.crypto_name}/stats"
            # try except - error handling
            try:
                data = requests.get(url)
            except:
                # return an error if request is invalid
                return "Error! Couldn't get data from requests url"
            return data
        else:
            # return an error if cryptoName isn't in the crypto list
            return "That isn't an available cryptocurrency"


def crypto_getter_blockchair(crypto_name: str, available_cryptos: list):
    crypto_stats = get_crypto_stats(crypto_name, available_cryptos)

    blockchair_response_data = crypto_stats.blockchair().json()['data']
    print(blockchair_response_data, flush=True)
    return blockchair_response_data


def cleanhtml(raw_html: str) -> str:
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def clean_time_range(posts: list, merits: list, dates: list, time_range: int) -> list:
    print("Clean Time range", flush=True)
    days_limit = datetime.now() - timedelta(days=time_range)
    posts_p, merits_p, dates_p = [], [], []
    remove_data_2d = []
    for date_list in dates:

        j = 0

        remove_date = []
        new_dates, new_post, new_merits = [], [], []
        for date_in in date_list:

            if date_in.find('Today'):

                month, year = date_in.split(',')[0], date_in.split(',')[1]
                date_string = f"{month}{year}"
                if parser.parse(date_string) < days_limit:
                    remove_date.append(j)  # indexes to remove

            j += 1

        remove_data_2d.append(remove_date)

        # removing dates that are over 7 days
    print(len(remove_data_2d), flush=True)
    for k in range(len(dates)):
        for b in range(len(dates[k])):
            # only add the ones that are in the time range and merits are over 500
            if b not in remove_data_2d[k] and int(merits[k][b]) > 500:
                new_merits.append(merits[k][b])
                new_post.append(posts[k][b])
                new_dates.append(dates[k][b])
        posts_p.append(new_post)
        merits_p.append(new_merits)
        dates_p.append(new_dates)

    return dates_p, posts_p, merits_p

# https://www.geeksforgeeks.org/python-sentiment-analysis-using-vader/ -> sentiment scores algo


def sentiment_scores(sentence: str) -> int:
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
    sid_obj.lexicon.update(new_words)

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        return 1  # positive

    elif sentiment_dict['compound'] <= - 0.05:
        return -1  # negative

    else:
        return 0  # neutral
    

def process_tweet(tweet):
    print("Process tweet", flush=True)
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')
    # remove stock market tickers like $GE
    input_text = re.sub(r'\$\w*', '', tweet)
    # remove old style reinput_text text "RT"
    input_text = re.sub(r'^RT[\s]+', '', input_text)
    # remove hyperlinks
    input_text = re.sub(r'https?:\/\/.*[\r\n]*', '', input_text)
    # remove hashtags
    # only removing the hash # sign from the word
    input_text = re.sub(r'#', '', input_text)
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    tweet_tokens = tokenizer.tokenize(input_text)

    tweets_clean = []
    for word in tweet_tokens:
        if (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation):  # remove punctuation
            # tweets_clean.append(word)
            stem_word = stemmer.stem(word)  # stemming word
            tweets_clean.append(stem_word)

    return tweets_clean


def build_freqs(tweets, ys):
    print("Build freqs", flush=True)
    # Convert np array to list since zip needs an iterable
    yslist = np.squeeze(ys).tolist()

    # Starts with empty dict, and append to it iterating over all tweets
    # and over all processed words in each tweet.
    freqs = {}
    for y, tweet in zip(yslist, tweets):
        for word in process_tweet(tweet):
            pair = (word, y)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1

    return freqs


def sigmoid(z):

    # 1 / ( 1 + e ^ -z)
    h = 1/(1+np.exp(-z))

    return h


def gradientDescent(x, y, theta, alpha, num_iters):
    print("Gradient descent", flush=True)
    # get 'm', the number of rows in matrix x
    m = x.shape[0]

    for i in range(0, num_iters):

        # get z, the dot product of x and theta
        z = np.dot(x, theta)

        # get the sigmoid of z
        h = sigmoid(z)

        # calculate the cost function
        J = -1./m * (np.dot(y.transpose(), np.log(h)) +
                     np.dot((1-y).transpose(), np.log(1-h)))

        # update the weights theta
        theta = theta - (alpha/m) * np.dot(x.transpose(), (h-y))

    J = float(J)
    return J, theta


def extract_features(tweet, freqs):
    print("extract features", flush=True)
    # process_tweet tokenizes, stems, and removes stopwords
    word_l = process_tweet(tweet)

    # 3 elements in the form of a 1 x 3 vector
    x = np.zeros((1, 3))

    # bias term is set to 1
    x[0, 0] = 1

    # loop through each word in the list of words
    for word in word_l:

        # increment the word count for the positive label 1
        x[0, 1] += freqs.get((word, 1.0), 0)

        # increment the word count for the negative label 0
        x[0, 2] += freqs.get((word, 0.0), 0)

    assert(x.shape == (1, 3))
    return x


def predict_text(text, freqs, theta):
    print("predict text...", flush=True)
    # extract the features of the tweet and store it into x
    x = extract_features(text, freqs)

    # make the prediction using x and theta
    y_pred = sigmoid(np.dot(x, theta))

    return y_pred


# bitcoin talk, getting the sentiments of the cryptomarket over a time range using a weighted average
# of logistic regression and vader sentiment
def bitcoin_talk(time_range: int):

    # bitcoin talk, bitcoin discussion board
    print("Getting Bitcointalk url", flush=True)
    url = "https://bitcointalk.org/index.php?board=1.0"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    topics_list_dup = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and 'topic' in href:
            topics_list_dup.append(str(href))

    # cleaning list
    topics_set = set()  # set of topic ids
    not_topics = ["20333", "5359781", "1649348"]  # pinned / irrelevant topics
    for topic in topics_list_dup:
        new_list = topic.split('=')
        if(len(new_list) == 2):
            topic_num = topic.split('=')[1].split('.')[0]
            if(topic_num not in not_topics):  # check if redundant
                topics_set.add(topic.split('=')[1].split('.')[
                               0])  # string templating
            pass
        else:
            # printing invalid hrefs
            print(f"Invalid href: {topic}", flush=True)

    links_to_discussion = []
    for topic in topics_set:
        links_to_discussion.append(
            f"https://bitcointalk.org/index.php?topic={topic}.0")

    post_strings = []
    date_strings = []
    author_strings = []
    i = 0

    print("Links in discussion getting and cleaning", flush=True)
    for link in links_to_discussion:
        print(f"{i+1}------------------{link}---------------------", flush=True)
        resp = requests.get(link)
        soup = BeautifulSoup(resp.text, "html.parser")
        # going through posts of discussion
        posts_list = soup.find_all('div', {"class": "post"})
        # going through dates of posts
        date_soup = soup.find_all('td', {"class": "td_headerandpost"})
        # gonig through author information
        author_soup = soup.find_all('td', {"class", "poster_info"})
        date_list = []
        for body in date_soup:
            date = body.find("div", {"class": "smalltext"})  # finding the date
            clean_date = cleanhtml(str(date))
            if not clean_date.isdigit():
                date_list.append(clean_date)
        date_strings.append(date_list)
        author_list = []
        for body in author_soup:
            index_merit = (str(body).find('Merit'))
            if index_merit:
                merit = (str(body)[index_merit:index_merit+20])
                clean_merit = merit.split('<')[0].replace('Merit:', '')
                author_list.append(clean_merit)
        j = 0
        clean_post_list = []
        removed_posts = []
        for post in posts_list:  # going through all posts
            clean_post = cleanhtml(str(post))
            if not clean_post.isdigit():  # only get valid posts
                clean_post_list.append(clean_post)
            else:
                removed_posts.append(j)
            j += 1

        post_strings.append(clean_post_list)
        # removing author id's who's posts have been cleaned
        new_author_list = []
        for k in range(len(author_list)):  # going through all author informatoin
            if k not in removed_posts:  # only get valid author info
                new_author_list.append(author_list[k])

        author_strings.append(new_author_list)
        i += 1
        if i == 25:
            break  # so that not *too* many posts are gotten

    new_dates, new_post, new_merits = clean_time_range(
        post_strings, author_strings, date_strings, time_range)

    print('Getting vader sentiments....', flush=True)
    vader_sentiments = []
    for k in range(len(new_post)):
        post_sentiments = []
        for c in range(len(new_post[k])):
            post_sentiments.append(int(sentiment_scores(str(new_post[k][c]))))
        if k == 100:
            break
        vader_sentiments.append(post_sentiments)

    # Logistic regresssion process
    from os import getcwd
    nltk.download('twitter_samples')
    nltk.download('stopwords')

    # select the set of positive and negative tweets
    all_positive_tweets = twitter_samples.strings('positive_tweets.json')
    all_negative_tweets = twitter_samples.strings('negative_tweets.json')

    # split the data into two pieces, one for training and one for testing (validation set)
    test_pos = all_positive_tweets[4000:]
    train_pos = all_positive_tweets[:4000]
    test_neg = all_negative_tweets[4000:]
    train_neg = all_negative_tweets[:4000]

    train_x = train_pos + train_neg
    test_x = test_pos + test_neg

    # combine positive and negative labels
    train_y = np.append(np.ones((len(train_pos), 1)),
                        np.zeros((len(train_neg), 1)), axis=0)
    test_y = np.append(np.ones((len(test_pos), 1)),
                       np.zeros((len(test_neg), 1)), axis=0)

    # Print the shape train and test sets
    print("train_y.shape = " + str(train_y.shape), flush=True)
    print("test_y.shape = " + str(test_y.shape), flush=True)

    freqs = build_freqs(train_x, train_y)

    # collect the features 'x' and stack them into a matrix 'X'
    X = np.zeros((len(train_x), 3))
    for i in range(len(train_x)):
        X[i, :] = extract_features(train_x[i], freqs)

    # training labels corresponding to X
    Y = train_y

    # Apply gradient descent
    J, theta = gradientDescent(X, Y, np.zeros((3, 1)), 1e-9, 1500)
    print(f"The cost after training is {J:.8f}.", flush=True)
    print(
        f"The resulting vector of weights is {[round(t, 8) for t in np.squeeze(theta)]}", flush=True)

    print('Getting Log Reg sentiments....', flush=True)
    log_reg_sentiments = []
    for k in range(len(new_post)):
        log_sentiments = []
        for c in range(len(new_post[k])):
            y_hat = predict_text(str(new_post[k][c]), freqs, theta)
            log_sentiments.append(round(y_hat[0][0], 5))
        if k == 100:
            break
        log_reg_sentiments.append(log_sentiments)

    print('Cleaning the dates....', flush=True)
    # make this an input, where used decides how many posts to gather the longer it will take for them
    dates_used = new_dates[:100]
    dates_list = []
    dates_set = []
    for date in dates_used:
        dates_set1 = set()
        dates_list1 = []
        for item in date:
            if (item.find("AM") or item.find("PM")) and item.find('Today'):
                month_day, year = item.split(',')[0], item.split(',')[1]
                date_string = f"{month_day}{year}"
                item = parser.parse(date_string)
            else:
                item = datetime.now()

            dates_set1.add(item)
            dates_list1.append(item)

        dates_set.append(dates_set1)
        dates_list.append(dates_list1)

        dict_list = []
        for date_item in dates_set:
            a = {}
            Dict = defaultdict(lambda: 0, a)
            for index, val in enumerate(date_item):
                new_val = val.strftime("%d/%m/%Y")
                n = 0
                for item_date in range(len(dates_list)):
                    for item_child in range(len(dates_list[item_date])):
                        if (val == dates_list[item_date][item_child]):
                            Dict[new_val] += (log_reg_sentiments[item_date][item_child]*0.4) + (
                                vader_sentiments[item_date][item_child]*0.6)
                            n += 1

                Dict[new_val] = Dict[new_val] / n

            dict_list.append(Dict)

    result = defaultdict(list)

    for to_merge in dict_list:
        for key, value in to_merge.items():
            result[key].append(value)

    for item in result:
        n = 0
        summ = 0
        for num in result[item]:
            summ += num
            n += 1
        result[item] = round(summ / n, 3)

    return result

# CRYPTOCURRENCY ANALYSER


def start_analyser_process(crypto_name: str, time_range: str):
    print('Starting analyser process....', flush=True)
    if(time_range == "1 week"):
        time_range_inp = 7
    elif(time_range == "2 week"):
        time_range_inp = 14
    elif(time_range == "3 week"):
        time_range_inp = 21
    elif(time_range == "1 month"):
        time_range_inp = 30
    else:
        time_range_inp = 1  # if user doesn't select a valid

    results_default_dict = bitcoin_talk(time_range_inp)
    print(results_default_dict, flush=True)
    results_dict = dict(results_default_dict)

    json_results = json.dumps(results_dict, indent=4)

    return json_results


def market_indicator():
    url = "https://alternative.me/crypto/fear-and-greed-index/"

# Twitter opinion leaders
