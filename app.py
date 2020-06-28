import http

from flask import Flask, request, jsonify
from newsapi import NewsApiClient

from newsclient import NewsClient

app = Flask(__name__)
news = NewsClient()


def fetch_news_based_on_sentiment(keyword, sentiment):
    fetch_news = news.get_news(keyword)
    positive_news = [each_news for each_news in fetch_news if each_news['sentiment'] == sentiment]
    return positive_news


@app.route('/positive/', methods=['POST'])
def get_results():
    keyword = request.form['keyword']  # getting input from user
    positive_news = fetch_news_based_on_sentiment(keyword, "positive")
    if len(positive_news) > 0:
        return jsonify(positive_news)
    else:
        return '', http.client.NO_CONTENT


@app.route('/neutral/', methods=['POST'])
def get_results():
    keyword = request.form['keyword']  # getting input from user
    neutral_news = fetch_news_based_on_sentiment(keyword, "neutral")
    if len(neutral_news) > 0:
        return jsonify(neutral_news)
    else:
        return '', http.client.NO_CONTENT


@app.route('/negative/', methods=['POST'])
def get_negative_results():
    keyword = request.form['keyword']  # getting input from user

    negative_news = fetch_news_based_on_sentiment(keyword, "negative")
    if len(negative_news) > 0:
        return jsonify(negative_news)
    else:
        return '', http.client.NO_CONTENT


if __name__ == '__main__':
    app.run()
