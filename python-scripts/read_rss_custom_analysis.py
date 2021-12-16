"""
read_rss_custom_analysis.py

An RSS analyzer that uses a custom Naive Bayes Classifier.
"""
from deephaven import Types as dht
from deephaven import DynamicTableWriter

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def _word_feats(words):
    """
    NLTK word feature generator for the NaiveBayesClassifier
    """
    return dict([(word, True) for word in words])

def _word_feats_string(strn):
    """
    NLTK word feature generator for the NaiveBayesClassifier that
    takes a string
    """
    return dict([(word, True) for word in strn.split(" ")])

def build_model():
    """
    Builds the NaiveBayesClassifier model
    """
    nltk.download('movie_reviews')

    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(_word_feats(movie_reviews.words(fileids=[f])), "negative") for f in negids]
    posfeats = [(_word_feats(movie_reviews.words(fileids=[f])), "positive") for f in posids]

    trainfeats = negfeats + posfeats

    return NaiveBayesClassifier.train(trainfeats)

def build_model_func(classifier):
    """
    Generates a method that classifies a string using the given classifier
    """
    def a(strn):
        return strn, classifier.classify(_word_feats_string(strn))
    return a

rss_feed_url = "https://www.reddit.com/r/wallstreetbets/new/.rss"
rss_attributes = [
    "title"
]
classifier = build_model_func(build_model())

column_names = [
    "Sentence",
    "Sentiment"
]
column_types = [
    dht.string,
    dht.string
]
custom_sia_table_writer = DynamicTableWriter(column_names, column_types)
custom_sia = custom_sia_table_writer.getTable()

thread = threading.Thread(target=read_rss, args=[rss_feed_url, rss_attributes, classifier, custom_sia_table_writer])
thread.start()
