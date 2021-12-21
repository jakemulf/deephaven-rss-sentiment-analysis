"""
read_rss_default_analysis.py

An RSS reader in Python that does sentiment analysis using the NLKT default sentiment analysis, and stores the results in Deephaven.

This file is meant to run through Deephaven's Application Mode as part of several Python scripts. Because of this, some
variables may not be defined in here, but instead in helper_functions.py or read_rss.py.
"""
from deephaven import as_list

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

def build_default_sia_classifier_func(classifier):
    def a(strn):
        sentiment = classifier.polarity_scores(strn)
        return as_list([sentiment["pos"], sentiment["neu"], sentiment["neg"], sentiment["compound"]])
    return a

rss_attributes = [
    "title"
]
classifier = build_default_sia_classifier_func(SentimentIntensityAnalyzer())

rss_feed_url = "https://www.reddit.com/r/wallstreetbets/new/.rss"
built_in_sia_wsb = read_rss(rss_feed_url, rss_attributes, datetime_converter_reddit)

rss_feed_url = "https://www.reddit.com/r/all/new/.rss"
built_in_sia_all = read_rss(rss_feed_url, rss_attributes, datetime_converter_reddit, sleep_time=1)

rss_feed_url = "https://hnrss.org/newest"
built_in_sia_hackernews = read_rss(rss_feed_url, rss_attributes, datetime_converter_hackernews, sleep_time=60)

built_in_sia_wsb = built_in_sia_wsb.update("Sentiment = classifier(Sentence)")
#    .update("Positive = Sentiment[0]")\
#    .update("Neutral = Sentiment[1]")\
#    .update("Negative = Sentiment[2]")\
#    .update("Compound = Sentiment[3]")
built_in_sia_all = built_in_sia_all.update("Sentiment = classifier(Sentence)")
#    .update("Positive = Sentiment[0]")\
#    .update("Neutral = Sentiment[1]")\
#    .update("Negative = Sentiment[2]")\
#    .update("Compound = Sentiment[3]")
built_in_sia_hackernews = built_in_sia_hackernews.update("Sentiment = classifier(Sentence)")
#    .update("Positive = Sentiment[0]")\
#    .update("Neutral = Sentiment[1]")\
#    .update("Negative = Sentiment[2]")\
#    .update("Compound = Sentiment[3]")
