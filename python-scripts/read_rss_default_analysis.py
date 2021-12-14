"""
read_rss_default_analysis.py

A simple rss reader in Python that does sentiment analysis and puts the built_in_sias in Deephaven
"""
import feedparser

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

from deephaven import DynamicTableWriter, Types as dht

RSS_FEED_URL = "https://www.reddit.com/r/reddit.com/new/.rss"
RSS_ATTRIBUTES_TO_ANALYZE = [
    "title"
]
COLUMN_NAMES = [
    "Positive",
    "Neutral",
    "Negative",
    "Compound",
    "Sentence"
]
COLUMN_TYPES = [
    dht.double,
    dht.double,
    dht.double,
    dht.double,
    dht.string
]

feed = feedparser.parse(RSS_FEED_URL)

sia = SentimentIntensityAnalyzer()
built_in_sia_table_writer = DynamicTableWriter(COLUMN_NAMES, COLUMN_TYPES)

built_in_sia = built_in_sia_table_writer.getTable()

for entry in feed.entries:
    for attribute in RSS_ATTRIBUTES_TO_ANALYZE:
        sentiment = sia.polarity_scores(entry[attribute])
        built_in_sia_table_writer.logRow(
            sentiment["pos"],
            sentiment["neu"],
            sentiment["neg"],
            sentiment["compound"],
            entry[attribute]
        )
