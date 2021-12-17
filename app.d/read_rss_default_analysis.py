"""
read_rss_default_analysis.py

A simple rss reader in Python that does sentiment analysis using the NLKT default sentiment analysis, and stores the results in Deephaven.
"""
from deephaven import DynamicTableWriter, Types as dht

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
    "Sentence"
]
column_types = [
    dht.double,
    dht.double,
    dht.double,
    dht.double,
    dht.string
]
built_in_sia_writer = DynamicTableWriter(column_names, column_types)
built_in_sia = built_in_sia_writer.getTable()

thread = threading.Thread(target=read_rss, args=[rss_feed_url, rss_attributes, classifier, built_in_sia_writer])
thread.start()
