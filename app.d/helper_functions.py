"""
helper_functions.py

A file that defines some shared helper functions and imports for the RSS readers.
"""
from deephaven import DynamicTableWriter, Types as dht
from deephaven.DateTimeUtils import convertDateTime

from dateutil import parser

from datetime import datetime

import threading

def datetime_converter_reddit(entry):
    dt = datetime.fromisoformat(entry["updated"])
    dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
    return convertDateTime(dts)

def datetime_converter_hackernews(entry):
    dt = parser.parse(entry["published"])
    dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
    return convertDateTime(dts)
