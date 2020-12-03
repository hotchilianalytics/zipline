#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os


from pathlib import Path
from zipline.data.bundles import register
from zipline.data.bundles.ingester import csv_ingester # ingester.py need to be placed in zipline.data.bundles

# _DEFAULT_PATH = str(Path.home() / '.zipline/csv/yahoo')
_DEFAULT_PATH = str(Path.home() / 'zipline-broker/data/csv/yahoo')  #HCA path

# HCA: Start
#    Setup start and end dates for bundle ingestion, Default period is two years.
#    Can be overridden by environment variables START_DATE, END_DATE

hca_root_path = os.environ['HCA_ROOT']
print(f"extension: hca_root_path = {hca_root_path}")

today_dt=pd.datetime.today()
TODAY_STR = today_dt.strftime("%Y-%m-%d")
print("extension:TODAY_STR = {}".format(TODAY_STR))

date_2yr_ago_dt = pd.datetime(today_dt.year-2, today_dt.month, today_dt.day)
TWO_YR_AGO_STR = date_2yr_ago_dt.strftime("%Y-%m-%d")
print("extension:TWO_YR_AGO_STR = {}".format(TWO_YR_AGO_STR))

start_date =  os.environ.get('START_DATE')
end_date   =  os.environ.get('END_DATE')
if not start_date:
    start_date = TWO_YR_AGO_STR
if not end_date:
    end_date = TODAY_STR

print("extension:  start_date={} end_date = {}".format(start_date, end_date))
# HCA: End
    
register(
    'yahoo_csv',
    csv_ingester('YAHOO',
                 every_min_bar=False, # the price is daily
                 csvdir_env='YAHOO_CSVDIR',
                 csvdir=_DEFAULT_PATH,
                 index_column='Date',
                 column_mapper={'Open': 'open',
                                'High': 'high',
                                'Low': 'low',
                                'Close': 'close',
                                'Volume': 'volume',
                                'Adj Close': 'price',
                 },
    ),
    calendar_name='NYSE',
)

from zipline.data.bundles.ingester import direct_ingester

from zipline.data.bundles import yahoo
register('yahoo_direct', # bundle's name
         direct_ingester('YAHOO',
                         every_min_bar=False,
                         symbol_list_env='YAHOO_SYM_LST', # the environemnt variable holding the comma separated list of assert names
                         downloader=yahoo.get_downloader(start_date=start_date,
                                                         end_date=end_date
                         #downloader=yahoo.get_downloader(start_date='2018-01-01',
                         #                                end_date='2020-11-30'
                         ),
         ),
         calendar_name='NYSE',
)

from zipline.data.bundles import iex
register('iex', # bundle's name
         direct_ingester('IEX Cloud',
                         every_min_bar=False,
                         symbol_list_env='IEX_SYM_LST', # the environemnt variable holding the comma separated list of assert names
                         downloader=iex.get_downloader(start_date=start_date,
                                                       end_date=end_date
                         ),
         ),
         calendar_name='NYSE',
)
