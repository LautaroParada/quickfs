# QuickFS API SDK

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://shields.io/) ![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

**Contents**

1. General description
2. Requirements
3. Installation
4. Demo
5. Documentation
6. Disclaimer

## General description
This library is the Python :snake: unofficial SDK for the QuickFS REST API. It's intended to be used for data extraction for financial valuations. 
## Requirements
- You need to request an API key with the QuickFS team. Create your account in the following [link](https://quickfs.net/)
- ```Python``` >= 3.8

## Installation
```python
```
## Demo
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

## Documentation

All the methods will use the following instance of the general class:
```python
from quickfs import QuickFS
import os

# load the key from the enviroment variables
api_key = os.environ['API_QUICKFS']
# client instance
client = QuickFS(api_key)
```

### Companies
- ```get_api_metadata```: 

- ```get_supported_companies```:Returns a list of ticker symbols supported by QuickFS.net. You may optionally specify a country code (US, CA, MM, AU, NZ, or LN) and an exchange. It is recommendable to use the get_api_metadata to get the references.
	- arguments:
		- country(str): code of the country to request data.
		- exchange(str): code of the exchange to request data.
	- Usage:
```python
# get the companies for the NYSE exchange
NYSE = client.get_supported_companies(country='US', exchange='NYSE')
# get the companies for the LSE
LSE = client.get_supported_companies(country='LN', exchange='LONDON')
# get the companies from Australia
ASX = resp = client.get_supported_companies(country='AU', exchange='ASX')
```

- ```get_updated_companies```: code of the exchange to request data.

### Metrics
- ```get_available_metrics```:

### Datapoints
- ```get_data_range```:

- ```get_data_full```:

- ```get_data_batch```:

### Usage history
- ```get_usage```:

## Disclaimer
The information in this document is for informational and educational purposes only. Nothing in this document may be construed as financial, legal or tax advice. The content of this document is solely the opinion of the author, who is not a licensed financial advisor or registered investment advisor. The author is not affiliated as a promoter of QuickFS services.

This document is not an offer to buy or sell financial instruments. Never invest more than you can afford to lose. You should consult a registered professional advisor before making any investment.