# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 16:00:22 2021

@author: lauta
"""

from quickfs import QuickFS
import os
import numpy as np

api_key = os.environ['API_QUICKFS']

client = QuickFS(api_key)

#%% Companies reference data

resp = client.get_api_metadata()
resp = client.get_supported_companies(country='US', exchange='NYSE')
random_company = np.random.choice(resp)
resp = client.get_updated_companies(country='US', date='20210420')

#%% Metrics

resp = client.get_available_metrics()
import pandas as pd
df = pd.DataFrame(resp)

# search for specific fields
df[df['metric'].str.contains('volume')]

#%% Datapoints

resp = client.get_data_range(symbol='AAPL:US', metric='shares_eop', period='FQ-15:FQ')
resp = client.get_data_full(symbol='AAPL:US')
resp = client.get_data_batch(companies=['KO:US', 'PEP:US'], metrics=['roa', 'roic'], period="FY-2:FY")

#%% Usage History

resp = client.get_usage()