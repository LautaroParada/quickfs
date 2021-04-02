# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 16:00:22 2021

@author: lauta
"""

from quickfs import QuickFS
import os

api_key = os.environ['API_QUICKFS']

client = QuickFS(api_key)

#%% Companies reference data

resp = client.get_companies_metadata(df=True)
resp = client.get_supported_companies(country='US', exchange='NYSE')
resp = client.get_updated_companies(country='US', date='20210315')