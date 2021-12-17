"""
read_rss_default_analysis.py

An RSS reader in Python that does sentiment analysis using the NLKT default sentiment analysis, and stores the results in Deephaven.

This file is meant to run through Deephaven's Application Mode as part of several Python scripts. Because of this, some
variables may not be defined in here, but instead in helper_functions.py.
"""
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

def build_default_sia_classifier_func(classifier):
    def a(strn):
        sentiment = classifier.polarity_scores(strn)
        return sentiment["pos"], sentiment["neu"], sentiment["neg"], sentiment["compound"], strn
    return a

rss_feed_url = "https://www.reddit.com/r/wallstreetbets/new/.rss"
rss_attributes = [
    "title"
]
classifier = build_default_sia_classifier_func(SentimentIntensityAnalyzer())

column_names = [
    "Positive",
    "Neutral",
    "Negative",
    "Compound",
    "Sentence",
    "Datetime"
]
column_types = [
    dht.double,
    dht.double,
    dht.double,
    dht.double,
    dht.string,
    dht.datetime
]
built_in_sia_wsb_writer = DynamicTableWriter(column_names, column_types)
built_in_sia_wsb = built_in_sia_wsb_writer.getTable()

thread_wsb = threading.Thread(target=read_rss, args=[rss_feed_url, rss_attributes, classifier, built_in_sia_wsb_writer, datetime_converter_reddit])
thread_wsb.start()

rss_feed_url = "https://www.reddit.com/r/all/new/.rss"
built_in_sia_all_writer = DynamicTableWriter(column_names, column_types)
built_in_sia_all = built_in_sia_all_writer.getTable()

thread_all = threading.Thread(target=read_rss, args=[rss_feed_url, rss_attributes, classifier, built_in_sia_all_writer, datetime_converter_reddit, 1])
thread_all.start()

rss_feed_url = "https://hnrss.org/newest"
built_in_sia_hackernews_writer = DynamicTableWriter(column_names, column_types)
built_in_sia_hackernews = built_in_sia_hackernews_writer.getTable()

thread_hackernews = threading.Thread(target=read_rss, args=[rss_feed_url, rss_attributes, classifier, built_in_sia_hackernews_writer, datetime_converter_hackernews, 60])
thread_hackernews.start()
