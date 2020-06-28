import re
import os
from newsapi import NewsApiClient
from textblob import TextBlob


class NewsClient(object):

    @staticmethod
    def clean_news(news):
        """
        Utility function to clean news title by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", news).split())

    def get_news_sentiment(self, news):
        """
        Utility function to classify sentiment of passed news
        using textblob's sentiment method
        """
        # create TextBlob object of passed news text
        analysis = TextBlob(self.clean_news(news))
        # set sentiment
        if analysis.sentiment.polarity > 0.5:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_news(self, keyword):
        """
        Main function to fetch news and parse them.
        """
        # empty list to store parsed news
        news_list = []
        api_key = os.getenv('API_KEY')

        newsapi = NewsApiClient(api_key=api_key)

        try:
            # call news api to fetch news
            fetched_news = newsapi.get_top_headlines(q=keyword,
                                                     # sources='bbc-news'
                                                     # category='health',
                                                     language='en')
            articles = fetched_news['articles']

            # parsing news one by one
            for each in articles:
                # empty dictionary to store required params of a news
                parsed_news = {}

                # saving text of news
                parsed_news['text'] = each['title']
                # saving sentiment of news
                parsed_news['sentiment'] = self.get_news_sentiment(each['title'])

                # appending parsed news to the list

                if parsed_news not in news_list:
                    news_list.append(parsed_news)

                # return parsed news
            return news_list
        except Exception as e:
            # print error (if any)
            print("Error : " + str(e))
