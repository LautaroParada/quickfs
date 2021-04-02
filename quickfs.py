# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:55:18 2021

@author: lauta
"""

import requests
from typing import Dict
import logging
import pandas as pd

class QuickFS():
    
    def __init__(self, api_key, timeout: int = 300):
        self.api_key = api_key
        self.timeout = timeout
        self.HOST = 'https://public-api.quickfs.net/v1'
        self.resp = None
        
        self.headers = {
                'X-QFS-API-Key': api_key
            }
        
        self.params = {
            }
        
        self.endpoint_pivot = None
        
        self.metadata = {
                'Country':[
                    'United States', 
                    'United States', 
                    'United States', 
                    'United States', 
                    'United States', 
                    'United States', 
                    'Canada',
                    'Canada',
                    'Canada',
                    'Australia', 
                    'New Zealand', 
                    'Mexico', 
                    'London'
                    ], 
                'Code': [
                    'US',
                    'US',
                    'US',
                    'US',
                    'US',
                    'US',
                    'CA',
                    'CA',
                    'CA',
                    'AU',
                    'NZ',
                    'MN', 
                    'LN'
                         ], 
                'Exchanges':[
                    'NYSE',
                    'NASDAQ',
                    'OTC',
                    'NYSEARCA',
                    'BATS',
                    'NYSEAMERICAN',
                    'TORONTO',
                    'CSE',
                    'TSXVENTURE',
                    'ASX',
                    'NZX',
                    'BMV',
                    'LONDON'
                    ]
                }
        
    def __handle_response(self):
        self.resp = requests.get(self.endpoint_pivot, headers=self.headers, timeout=self.timeout)
            
        if self.resp.status_code == 200:
             if 'data' in self.resp.json().keys():
                 return self.resp.json()['data']
             else:
                 return self.resp.json()
        else:
            self.resp.raise_for_status()
            
    def __endpoint_builder(self, endpoint: str):
        self.endpoint_pivot = f"{self.HOST}{endpoint}"
            
    # ------------------------------
    # Companies
    # ------------------------------
    
    def get_supported_companies(self, country: str, exchange: str):
        """
        Returns a list of ticker symbols supported by QuickFS.net. You may 
        optionally specify a country code (US, CA, MM, AU, NZ, or LN) and 
        an exchange.

        Parameters
        ----------
        **query_params : dict
            country and exchange to use for filtering.

        Returns
        -------
        ticker symbols.

        """            
        self.__endpoint_builder(f"/companies/{country}/{exchange}")
        return self.__handle_response()
    
    
    def get_companies_metadata(self, df:bool = False):
        """
        Returns the available countries and exchanges where to get data.

        Parameters
        ----------
        df : bool, optional
            Return as a dataframe or dictionary. The default is False.

        Returns
        -------
        dict
            available countries and exchanges.

        """
        if df:
            return pd.DataFrame(self.metadata)
        else:
            return self.metadata
        
    
    def get_updated_companies(self, country: str, date: str):
        """
        Returns a list of ticker symbols that were updated with new financial
        data on or after the specified date (formatted as YYYYMMDD). You may
        optionally specify a country code (US, CA, MM, AU, NZ, or LN).

        Parameters
        ----------
        country : str
            country to use as a filter.
        date : str
            YYYYMMDD format.

        Returns
        -------
        dict
            list of companies with updated financial statements.

        """
        self.__endpoint_builder(f"/companies/updated/{date}/{country}")
        return self.__handle_response()