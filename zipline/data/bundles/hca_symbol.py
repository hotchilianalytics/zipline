"""
Module for building a complete daily dataset from Quandl's Sharadar dataset.
"""
from io import BytesIO
import tarfile
from zipfile import ZipFile

from click import progressbar
from logbook import Logger
import pandas as pd
import requests
from six.moves.urllib.parse import urlencode
from six import iteritems
from trading_calendars import register_calendar_alias

from zipline.utils.deprecate import deprecated
from zipline.data.bundles import core as bundles  # looking in .zipline/extensions.py
#from . import core as bundles
import numpy as np

# Code from:
    # Quantopian Zipline Issues:
    # "Cannot find data bundle during ingest #2275"
    #https://github.com/quantopian/zipline/issues/2275

log = Logger(__name__)

@bundles.register('hca-symbol')
def hca_symbol_bundle(environ,
                  asset_db_writer,
                  minute_bar_writer,
                  daily_bar_writer,
                  adjustment_writer,
                  calendar,
                  start_session,
                  end_session,
                  cache,
                  show_progress,
                  output_dir):
    
    log.info("Processing hca-symbol bundle.")    


#register_calendar_alias("QUANDL", "NYSE")
register_calendar_alias("hca-symbol", "NYSE")
