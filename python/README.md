# Binance Pay API signature in Python


## How to run

The code is written in python with minimual dependencies, only the `requests` package is required.

```python

# install the dependency page
pip install requests

```

## Setup the API key and secret

The API key and secret are required for working on Binance Pay API. It can be generated from:
https://merchant.binance.com/en/dashboard/developers <br/>

Then set them into the `merchant.py`. 
<br/>

There are 2 methods available in the code for testing: <br/>
- `query_order`
- `create_order`

Please feel free to add your own method to experience more endpoints.

```python
python merchant.py
```
