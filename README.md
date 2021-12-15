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
