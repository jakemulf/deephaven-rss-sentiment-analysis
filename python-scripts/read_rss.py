"""
read_rss.py

Defines the method for reading from an RSS feed and performing sentiment analysis on the data.
"""
import feedparser

import time
import threading
from datetime import datetime

def read_rss(rss_feed_url, rss_attributes, classifier, sia_table_writer, sleep_time=5):
    """
    This method continually reads from an RSS feed and stores its data, along with
    sentiment analysis on the data, in a Deephaven table.

    Data is only written to the Deephaven table if it's new data.

    Parameters:
        rss_feed_url (str): The RSS feed URL as a string.
        rss_attributes (list<str>): A list of attributes from the RSS feed to analyze.
        classifier (method): A method that takes a string and returns the desired classification for the string. The
            returned values of this method are converted to a row in the Deephaven table, so those attributes
            need to match.
        sia_table_writer (deephaven.DynamicTableWriter): The dynamic table writer for the table.
        sleep_time (int): An integer representing the number of seconds to wait between
            RSS pulls if data hasn't changed.

    Returns:
        None
    """
    last_updated = None

    while True:
        feed = feedparser.parse(rss_feed_url)

        i = 0
        while i < len(feed.entries):
            entry = feed.entries[i]

            #If data has previously been read, and the current item has a timestamp less than or equal
            #to the last item written to the table in the previous pull, then stop writing data.
            #RSS feeds can unpublish data, so a strict equality comparison can't work.
            #This may result in lost data if the RSS feed can publish multiple items with the same timestamp.
            if not (last_updated is None) and datetime.fromisoformat(entry["updated"]) <= datetime.fromisoformat(last_updated):
                break

            for attribute in rss_attributes:
                sia_table_writer.logRow(
                    classifier(entry[attribute])
                )

            i += 1

        if i == 0: #Feed hasn't been updated, sleep
            time.sleep(sleep_time)
        else: #Otherwise set last updated time to the newest item in the feed
            last_updated = feed.entries[0]["updated"]
