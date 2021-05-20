# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:55:18 2021

@author: lauta
"""

import requests
from typing import Dict, List
import logging

class QuickFS():
    
    def __init__(self, api_key, timeout: int = 300):
        self.api_key = api_key
        self.timeout = timeout
        self.HOST = 'https://public-api.quickfs.net/v1'
        self.resp = None
        
        self.headers = {
                'X-QFS-API-Key': api_key
            }
        
        self.endpoint_pivot = None
        
        self.QUICKFS_KEYS = [
                'data',
                'usage'
            ]
        
        self.keys_bool = False
        self.response_key = None
        
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
                    'MM', 
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
        
        self.query_params_names = [
                "period"
            ]
        
        self.name_error = False
        
        self.request_body = None
        self.test = None
        
    
    def __handle_response(self, query_params: Dict[str, str]={}):
        
        if self.request_body is None:
            self.resp = requests.get(self.endpoint_pivot, 
                                     params=query_params, 
                                     headers=self.headers, 
                                     timeout=self.timeout)
        else:
            self.resp = requests.post(self.endpoint_pivot,
                                     json=self.request_body,
                                     headers=self.headers,
                                     timeout=self.timeout)
            
            self.request_body = None
            
            
        self.__response_key_finder(self.resp)
            
        if self.resp.status_code == 200:
            self.keys_bool = False
            return self.resp.json()[self.response_key]
            
        else:
            self.resp.raise_for_status()
            
    
    def __endpoint_builder(self, endpoint: str):
        self.endpoint_pivot = f"{self.HOST}{endpoint}"
        
    
    def __param_checker(self, items_):
        for key, value in items_:
            if key not in self.query_params_names:
                logging.error(f"The parameter {key} is not valid.")
                self.name_error = True
                
    def __response_key_finder(self, response):
        for key, value in response.json().items():
            if key in self.QUICKFS_KEYS:
                self.keys_bool = True
                self.response_key = key
            else:
                self.keys_bool = False
                
    def __handler_request_body(self, companies, metrics, period):
        self.request_body = {
            "data":{
                metric: {
                    company: f"QFS({company},{metric},{period})" for company in companies
                    } for metric in metrics
                }
            }
            
    # ------------------------------
    # Companies
    # ------------------------------
    
    def get_supported_companies(self, country: str, exchange: str):
        """
        Returns a list of ticker symbols supported by QuickFS.net. You may 
        optionally specify a country code (US, CA, MM, AU, NZ, or LN) and an 
        exchange.

        Parameters
        ----------
        country : str
            code of the country to request data.
        exchange : str
            code of the exchange to request data.

        Returns
        -------
        list
            available tickers for the country exchange.

        """           
        self.__endpoint_builder(f"/companies/{country}/{exchange}")
        return self.__handle_response()
    
    
    def get_api_metadata(self, df:bool = False):
        """
        Returns the available countries and exchanges where to get data.

        Parameters
        ----------
        df : bool, optional
            Return as a dataframe or dictionary. The default is False.

        Returns
        -------
        dict or pandas.DataFrame
            available countries and exchanges.

        """
        return self.metadata
        
    
    def get_updated_companies(self, country: str, date: str):
        """
        Returns a list of ticker symbols that were updated with new financial
        data on or after the specified date (formatted as YYYYMMDD). You may
        specify a country code (US, CA, MM, AU, NZ, or LN).

        Parameters
        ----------
        country : str
            country to use as a filter.
        date : str
            YYYYMMDD format.

        Returns
        -------
        list
            list of companies with updated financial statements.

        """
        self.__endpoint_builder(f"/companies/updated/{date}/{country}")
        return self.__handle_response()
    
    
    # ------------------------------
    # Metrics
    # ------------------------------
    
    def get_available_metrics(self):
        """
        Returns a list of available metrics with the associated metadata

        Returns
        -------
        dict
            available metrics
            
        """
        self.__endpoint_builder("/metrics")
        return self.__handle_response()
    
    
    # ------------------------------
    # Datapoints
    # ------------------------------
    
    def get_data_range(self, symbol: str, metric: str, **query_params):
        """
        Returns range of datapoints for a single company metric.

        Parameters
        ----------
        symbol : str
            Company symbol or qfs_symbol.
        metric : str
            QuickFS metric name.

        Returns
        -------
        list
            datapoints for a single company metric.

        """
        self.__endpoint_builder(f"/data/{symbol.upper()}/{metric.lower()}")
        
        self.__param_checker(items_=query_params.items())
        
        if self.name_error:
            self.name_error = False
            return
        
        return self.__handle_response(query_params)
    
    
    def get_data_full(self, symbol: str):
        """
        Pull metadata and all financial statements (annual and quarterly) for
        all periods for a single stock in one API call.

        Parameters
        ----------
        symbol : str
            Company symbol or qfs_symbol.

        Returns
        -------
        type
            metadata fields for the selected company.

        """
        self.__endpoint_builder(f"/data/all-data/{symbol.upper()}")
        return self.__handle_response()
    
    
    def get_data_batch(self, companies: List[str], metrics: List[str], period: str):
        """
        batch request for several companies retrieving multiple metrics.

        Parameters
        ----------
        companies : List[str]
            list of companies to query.
        metrics : List[str]
            list of metrics to query.
        period : str
            Period or period range.

        Returns
        -------
        dict
            data for the selected companies and metrics.

        """
        self.__handler_request_body(companies=companies, metrics=metrics, period=period)
        self.__endpoint_builder("/data/batch")
        return self.__handle_response()
    
    # ------------------------------
    # Usage History
    # ------------------------------
    
    def get_usage(self):
        """
        Returns your current API usage and limits

        Returns
        -------
        dict
            usage and limits for account.

        """
        self.__endpoint_builder("/usage")
        return self.__handle_response()