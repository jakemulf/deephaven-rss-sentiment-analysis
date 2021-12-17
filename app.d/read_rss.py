"""
read_rss.py

Defines the method for reading from an RSS feed and performing sentiment analysis on the data.
"""
import feedparser

import time
import threading

def read_rss(rss_feed_url, rss_attributes, classifier, sia_table_writer, datetime_converter, sleep_time=5):
    """
    This method continually reads from an RSS feed and stores its data, along with
    sentiment analysis on the data, in a Deephaven table.

    Data is only written to the Deephaven table if it's new data.

    Parameters:
        rss_feed_url (str): The RSS feed URL as a string.
        rss_attributes (list<str>): A list of attributes from the RSS feed to analyze.
        classifier (method): A method that takes a string and returns the desired classification for the string. The
            returned values of this method are converted to a row in the Deephaven table (except for the datetime),
            so those attributes need to match.
        sia_table_writer (deephaven.DynamicTableWriter): The dynamic table writer for the table. This writer can expect to
            write an arbitrary amount of items in a row. However, the last entry in the row must be a Deephaven datetime object.
        datetime_converter (method): A method that takes an RSS feed entry and converts it to a Deephaven datetime object.
            This should be customized based on the RSS feed.
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
            if not (last_updated is None) and datetime_converter(entry) <= last_updated:
                break

            for attribute in rss_attributes:
                write_attributes = classifier(entry[attribute]) #Returns a tuple
                datetime_attribute = (datetime_converter(entry),) #Need to convert return to a tuple
                
                #Since we can write an arbitrary number of items, we
                #need to unpack the 2 tuples
                write_row = (*write_attributes, *datetime_attribute)

                sia_table_writer.logRow(
                    write_row
                )

            i += 1

        if i == 0: #Feed hasn't been updated, sleep
            time.sleep(sleep_time)
        else: #Otherwise set last updated time to the newest item in the feed
            last_updated = datetime_converter(feed.entries[0])
