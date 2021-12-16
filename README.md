# deephaven-rss-sentiment-analysis

This app pulls data from an RSS feed, performs sentiment analysis on the data, and stores it in Deephaven for further analysis.

## Components

### General

* [`start.sh`](start.sh) - A helper script to launch the application.
* [`docker-compose.yml`](docker-compose.yml) - The Docker compose file that defines the Deephaven images.
* [`requirements.txt`](requirements.txt) - The Python dependencies for the app.

### Python scripts

* [`read_rss_default_analysis.py`](read_rss_default_analysis.py) - An RSS reader that uses NLKT's default sentiment analysis.
* [`read_rss_custom_analysis.py`](read_rss_custom_analysis.py) - An RSS reader that uses a user-defined sentiment analysis.
* [`queries.py`](queries.py) - Queries to run in Deephaven for extra analysis on the data.

## High level overview

This app pulls RSS data from a specified RSS feed using Python's [feedparser](https://pypi.org/project/feedparser/) package. When data is pulled, sentiment analysis is performed on attributes of the RSS data and stored in a Deephaven table. Deephaven table operations are then used to further analyze the data.

This app shows two examples of sentiment analysis, one using the default analyzer from [NLTK](https://www.nltk.org/), and one using an analyzer trained from NLTK's built in data.

By default, this app pulls from a Reddit RSS feed and performs sentiment analysis on the title of each post. The feed and attributes to analyze are customizable, so feel free to use this app to look at any RSS feed!
