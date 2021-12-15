"""
read_rss.py

A simple RSS reader with pulling logic
"""
from deephaven import DynamicTableWriter, Types as dht

import feedparser

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

import time
import threading
from datetime import datetime

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

sia = SentimentIntensityAnalyzer()

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
                sentiment = sia.polarity_scores(entry[attribute])
                built_in_sia_writer.logRow(
                    sentiment["pos"],
                    sentiment["neu"],
                    sentiment["neg"],
                    sentiment["compound"],
                    entry[attribute]
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
