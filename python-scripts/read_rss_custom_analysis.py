"""
read_rss_custom_analysis.py

An RSS analyzer that uses a custom Naive Bayes Classifier
"""
import feedparser

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

from deephaven import DynamicTableWriter, Types as dht

RSS_FEED_URL = "https://www.reddit.com/r/reddit.com/new/.rss"
RSS_ATTRIBUTES_TO_ANALYZE = [
    "title"
]

COLUMN_NAMES = [
    "Sentence",
    "Sentiment"
]
COLUMN_TYPES = [
    dht.string,
    dht.string
]

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

feed = feedparser.parse(RSS_FEED_URL)
custom_sia_writer = DynamicTableWriter(COLUMN_NAMES, COLUMN_TYPES)
custom_sia = custom_sia_writer.getTable()

for entry in feed.entries:
    for attribute in RSS_ATTRIBUTES_TO_ANALYZE:
        custom_sia_writer.logRow(
            entry[attribute],
            classifier(entry[attribute])
        )
