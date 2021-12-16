"""
read_rss_custom_analysis.py

An RSS analyzer that uses a custom Naive Bayes Classifier
"""
import feedparser

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

from deephaven import DynamicTableWriter, Types as dht

import time
import threading
from datetime import datetime

def word_feats(words):
    return dict([(word, True) for word in words])

def word_feats_string(strn):
    return dict([(word, True) for word in strn.split(" ")])

def build_model():
    nltk.download('movie_reviews')

    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), "negative") for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), "positive") for f in posids]

    trainfeats = negfeats + posfeats

    return NaiveBayesClassifier.train(trainfeats)

def build_model_func(classifier):
    def a(strn):
        return classifier.classify(word_feats_string(strn))
    return a

classifier = build_model_func(build_model())


column_names = [
    "Sentence",
    "Sentiment"
]
column_types = [
    dht.string,
    dht.string
]
custom_sia_writer = DynamicTableWriter(column_names, column_types)
custom_sia = custom_sia_writer.getTable()

def read_rss(rss_feed_url, rss_attributes, sleep_time=5):
    last_updated = None

    while True:
        feed = feedparser.parse(rss_feed_url)

        i = 0
        while i < len(feed.entries):
            entry = feed.entries[i]

            if not (last_updated is None) and datetime.fromisoformat(entry["updated"]) <= datetime.fromisoformat(last_updated):
                break

            for attribute in rss_attributes:
                custom_sia_writer.logRow(
                    entry[attribute],
                    classifier(entry[attribute])
                )

            i += 1

        if i == 0: #Feed hasn't been updated, sleep
            time.sleep(sleep_time)
        else: #Otherwise set last updated time to the newest item in the feed
            last_updated = feed.entries[0]["updated"]

rss_feed_url = "https://www.reddit.com/r/wallstreetbets/new/.rss"
rss_attributes = [
    "title"
]
thread = threading.Thread(target=read_rss, args=[rss_feed_url, rss_attributes])
thread.start()
