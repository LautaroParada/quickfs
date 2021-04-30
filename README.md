# QuickFS API SDK

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://shields.io/) ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

**Contents**

1. [General description](#general-description-arrow_up)
2. [Requirements](#requirements-arrow_up)
3. [Installation](#installation-arrow_up)
4. [Demo](#demo-arrow_up)
5. [Documentation](#documentation-arrow_up)
	- [Companies](#companies-arrow_up)
	- [Metrics](#metrics-arrow_up)
	- [Datapoints](#datapoints-arrow_up)
	- [Usage history](#usage-history-arrow_up)
6. [Disclaimer](#disclaimer-arrow_up)

## General description [:arrow_up:](#quickfs-api-sdk)
This library is the Python :snake: unofficial SDK for the QuickFS REST API. It's intended to be used for data extraction for financial valuations. 
## Requirements [:arrow_up:](#quickfs-api-sdk)
- You need to request an API key with the QuickFS team. Create your account in the following [link](https://quickfs.net/)
- ```Python``` >= 3.8

## Installation [:arrow_up:](#quickfs-api-sdk)
```python
```
## Demo [:arrow_up:](#quickfs-api-sdk)
The endpoints of the API will let you request fundamental data for your financial valuation. Here is a demo of its use:

```python
from quickfs import QuickFS
import os

# load the key from the enviroment variables
api_key = os.environ['API_QUICKFS']

client = QuickFS(api_key)

# Request reference data for the supported companies
resp = client.get_api_metadata()
resp = client.get_supported_companies(country='US', exchange='NYSE')
resp = client.get_updated_companies(country='US', date='20210420')

# Available metrics in the API
resp = client.get_available_metrics()

# Request fundamental data for each company
resp = client.get_data_range(symbol='AAPL:US', metric='shares_eop', period='FQ-15:FQ')
resp = client.get_data_full(symbol='AAPL:US')
resp = client.get_data_batch(companies=['KO:US', 'PEP:US'], metrics=['roa', 'roic'], period="FY-2:FY")

# Usage history
resp = client.get_usage()
```
*tutorial on how to save and load environment variables in Python -> [Hiding Passwords and Secret Keys in Environment Variables (Windows)](https://youtu.be/IolxqkL7cD8)*

## Documentation [:arrow_up:](#quickfs-api-sdk)

All the methods will use the following instance of the general class:
```python
from quickfs import QuickFS
import os

# load the key from the enviroment variables
api_key = os.environ['API_QUICKFS']
# client instance
client = QuickFS(api_key)
```

### Companies [:arrow_up:](#quickfs-api-sdk)
- ```get_api_metadata```: Returns the available countries and exchanges where to get data.
	- **arguments:*** ```None```
	- **usage:**
```python
# get the metadata for the countries and exchanges.
client.get_api_metadata()
```

- ```get_supported_companies```: Returns a list of ticker symbols supported by QuickFS. You need to specify a country code (US, CA, MM, AU, NZ, MN, or LN). It is recommendable to use the ```get_api_metadata``` to get the references for each argument.
	- **arguments:**
		- country(*str*): quickfs code of the country to request data.
		- exchange(*str*): quickfs code of the exchange to request data.
	- **usage:**
```python
# get the companies for the NYSE exchange
NYSE = client.get_supported_companies(country='US', exchange='NYSE')
# get the companies for the LSE
LSE = client.get_supported_companies(country='LN', exchange='LONDON')
# get the companies from Australia
ASX = resp = client.get_supported_companies(country='AU', exchange='ASX')
```

- ```get_updated_companies```: Returns a list of ticker symbols that were updated with new financial data on or after the specified date (formatted as YYYYMMDD). You need to specify a country code (US, CA, MM, AU, NZ, MN, or LN).
	- **arguments:**
		- country(*str*): quickfs code of the country to request data.
		- date(*str*): specific date to request data, it should be written in the following format YYYYMMDD. Please be aware that may be a delay in the company update and the actual update in the quickfs database.
	- **usage**
```python
# get the updated companies from New Zeland
client.get_updated_companies(country='NZ', date='20210420')
```

### Metrics [:arrow_up:](#quickfs-api-sdk)
- ```get_available_metrics```: Returns a list of available metrics with the associated metadata.
	- **arguments:** ```None```
	- **usage:**
```python
# get the supported metrics by quickfs
client.get_available_metrics()
```

### Datapoints [:arrow_up:](#quickfs-api-sdk)
It is highly recommendable to use the country identifier code for non-U.S. stocks. If you do not specify a country, the API will first try to match a U.S.-listed symbol and, if none is found, will then match with a non-U.S. company with the same symbol. The order of the returned data is from oldest to more recent data. 

Additionally, the period or period range to query should have the following structure ```period``` or ```from:to``` respectively. For example, revenue is reported quarterly and annually, as determined by a company's fiscal calendar. ```FY-9:FY``` represents the last 10 years of annual revenue figures. Similarly, the last 20 quarters of reported quarterly revenue is characterised by the periods ```FQ-19:FQ```.

- ```get_data_range```: Returns range of data points for a single company metric.
	- **arguments:**
		- symbol(*str*): company symbol. for example: AAPL:US
		- metric(*str*): QuickFS metric name.
	- **usage:**
```python
# get the shares outstanding (shares that have been authorized, issued, and purchased by investors and are held by them).
client.get_data_range(symbol='AAPL:US', metric='shares_eop', period='FQ-15:FQ')
```

- ```get_data_full```: Pull metadata and all financial statements (annual and quarterly) for all periods for a single stock in one API call.
	- **arguments:**
		- symbol(*str*): company symbol. for example: AAPL:US
	- **usage:**
```python
# get the full data for finnCap Group plc
client.get_data_full(symbol='FCAP:LN')
```

- ```get_data_batch```: Batch request for several companies retrieving multiple metrics.
	- **arguments:**
		- companies(*List[str]*): List of companies to query.
		- metrics(*List[str]*): List of metrics to query.
		- period(*str*): Period or period range to query.
	- **usage:**
```python
# Get the last 3 years of ROA and ROIC for Cocacola and Pepsi
client.get_data_batch(companies=['KO:US', 'PEP:US'], metrics=['roa', 'roic'], period="FY-2:FY")
```


### Usage history [:arrow_up:](#quickfs-api-sdk)
- ```get_usage```:  Returns your current API usage and limits.
	- **arguments:** ```None```
	- **usage:**
```python
client.get_usage()
```


## Disclaimer [:arrow_up:](#quickfs-api-sdk)
The information in this document is for informational and educational purposes only. Nothing in this document may be construed as financial, legal or tax advice. The content of this document is solely the opinion of the author, who is not a licensed financial advisor or registered investment advisor. The author is not affiliated as a promoter of QuickFS services.

This document is not an offer to buy or sell financial instruments. Never invest more than you can afford to lose. You should consult a registered professional advisor before making any investment.