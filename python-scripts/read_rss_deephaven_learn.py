"""
read_rss_deephaven_learn.py

An RSS reader that uses Deephaven learn to build a Naive Bayes Classifier.

Not ready yet
"""
import feedparser

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

from deephaven.learn import gather
from deephaven import learn
from deephaven import DynamicTableWriter, Types as dht

import numpy as np

RSS_FEED_URL = "https://www.reddit.com/r/reddit.com/new/.rss"
RSS_ATTRIBUTES_TO_ANALYZE = [
    "title"
]

COLUMN_NAMES = [
    "Sentence"
]
COLUMN_TYPES = [
    dht.string
]

def word_feats(words):
    d = dict([(word, True) for word in words])
    return d

def word_feats_string(strn):
    d = dict([(word, True) for word in strn.split(" ")])
    return d

def build_model():
    nltk.download('movie_reviews')

    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 0) for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 1) for f in posids]

    trainfeats = negfeats + posfeats

    return (NaiveBayesClassifier.train(trainfeats), len(trainfeats))

def build_model_func(classifier):
    def a(strn):
        return classifier.classify(word_feats_string(strn))
    return a

def table_to_numpy(rows, columns):
    return gather.table_to_numpy_2d(rows, columns, dtype=str)

def numpy_to_table(data, idx):
    return data[idx]

feed = feedparser.parse(RSS_FEED_URL)
rss_feed_table_writer = DynamicTableWriter(COLUMN_NAMES, COLUMN_TYPES)
rss_feed_table = rss_feed_table_writer.getTable()

for entry in feed.entries:
    for attribute in RSS_ATTRIBUTES_TO_ANALYZE:
        rss_feed_table_writer.logRow(
            [entry[attribute]]
        )

(classifier, batch_size) = build_model()

model_func = build_model_func(classifier)

inputs = [learn.Input(["Sentence"], table_to_numpy)]
outputs = [learn.Output("Sentiment", numpy_to_table, "String")]

result = learn.learn(
    table = rss_feed_table,
    model_func = model_func,
    inputs = inputs,
    outputs = outputs,
    batch_size = batch_size
)
