"""
read_rss.py

Defines the method for reading from an RSS feed and performing sentiment analysis on the data.
"""
import feedparser
from deephaven import DynamicTableWriter, Types as dht
from deephaven.DateTimeUtils import convertDateTime, currentTime
from dateutil import parser

import time

import threading

def _default_rss_attributes_method(entry):
    return [entry["title"]]

def _default_rss_datetime_converter(entry):
    try:
        dt = parser.parse(entry["published"])
        dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
        return convertDateTime(dts)
    except:
        return currentTime()

def read_single_rss_entry(rss_feed_url):
    """
    This method returns a single entry from the given RSS feed. This is mostly used
    for debugging and simple testing.

    Parameters:
        rss_feed_url (str): The RSS feed URL as a string.

    Returns:
        dict: A single entry from the RSS feed.
    """
    return feedparser.parse(rss_feed_url).entries[0]


def read_rss_static(rss_feed_url, rss_attributes_method=None, rss_datetime_converter=None):
    """
    This methods reads from an RSS feed once and stores its data
    
    Parameters:
        rss_feed_url (str): The RSS feed URL as a string.
        rss_attributes_method (method): A method that converts an RSS entry to a list of Strings to analyze. This should be
            customized based on the RSS feed.
        rss_datetime_converter (method): A method that takes an RSS feed entry and converts it to a Deephaven datetime object.
            This should be customized based on the RSS feed.

    Returns:
        Table: The Deephaven table that will contain the results from the RSS feed.
    """
    if rss_attributes_method is None:
        rss_attributes_method = _default_rss_attributes_method
    if rss_datetime_converter is None:
        rss_datetime_converter = _default_rss_datetime_converter

    feed = feedparser.parse(rss_feed_url)

    column_names = [
        "Sentence",
        "Datetime"
    ]
    column_types = [
        dht.string,
        dht.datetime
    ]
    table_writer = DynamicTableWriter(column_names, column_types)

    i = 0
    while i < len(feed.entries):
        entry = feed.entries[i]
        datetime_attribute = rss_datetime_converter(entry)

        for attribute in rss_attributes_method(entry):
            table_writer.logRow(
                attribute,
                datetime_attribute
            )

        i += 1

    return table_writer.getTable()

def read_rss_continual(rss_feed_url, rss_attributes_method=None, rss_datetime_converter=None, sleep_time=5):
    """
    This method continually reads from an RSS feed and stores its data in a Deephaven table.

    Data is only written to the Deephaven table if it's new data. This is determined by the timestamp of the entries.

    This method works best with RSS feeds that are always ordered by date-time, and update frequently. Some
    examples of this are Reddit and Hackernews RSS feeds. If you're unsure if your RSS feed will work, you can
    play it safe and use the read_rss_static() method and build your own method.

    Parameters:
        rss_feed_url (str): The RSS feed URL as a string.
        rss_attributes_method (method): A method that converts an RSS entry to a list of Strings to analyze. This should be
            customized based on the RSS feed.
        rss_datetime_converter (method): A method that takes an RSS feed entry and converts it to a Deephaven datetime object.
            This should be customized based on the RSS feed.
        sleep_time (int): An integer representing the number of seconds to wait between
            RSS pulls if data hasn't changed.

    Returns:
        Table: The Deephaven table that will contain the results from the RSS feed.
    """
    def thread_function(rss_feed_url, rss_attributes_method, rss_datetime_converter, sleep_time, table_writer):
        last_updated = None

        while True:
            feed = feedparser.parse(rss_feed_url)

            i = 0
            while i < len(feed.entries):
                entry = feed.entries[i]
                datetime_attribute = rss_datetime_converter(entry)

                #If no datetime, break
                if datetime_attribute is None:
                    break

                #If data has previously been read, and the current item has a timestamp less than or equal
                #to the last item written to the table in the previous pull, then stop writing data.
                #RSS feeds can unpublish data, so a strict equality comparison can't work.
                #This may result in lost data if the RSS feed can publish multiple items with the same timestamp.
                if not (last_updated is None) and datetime_attribute <= last_updated:
                    break

                for attribute in rss_attributes_method(entry):
                    table_writer.logRow(
                        attribute,
                        datetime_attribute
                    )

                i += 1

            if i == 0: #Feed hasn't been updated, sleep
                time.sleep(sleep_time)
            else: #Otherwise set last updated time to the newest item in the feed
                last_updated = rss_datetime_converter(feed.entries[0])

    column_names = [
        "Sentence",
        "Datetime"
    ]
    column_types = [
        dht.string,
        dht.datetime
    ]
    table_writer = DynamicTableWriter(column_names, column_types)

    if rss_attributes_method is None:
        rss_attributes_method = _default_rss_attributes_method
    if rss_datetime_converter is None:
        rss_datetime_converter = _default_rss_datetime_converter

    thread = threading.Thread(target=thread_function, args=[rss_feed_url, rss_attributes_method, rss_datetime_converter, sleep_time, table_writer])
    thread.start()

    return table_writer.getTable()
