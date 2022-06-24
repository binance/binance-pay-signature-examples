# Binance Pay API signature in Python


## How to run

The code is written in python with minimal dependencies, only the `requests` package is required.

```bash

# install the dependency page
pip install requests

```

## Setup the API key and secret

The API key and secret are required for working on Binance Pay API. It can be generated from:
https://merchant.binance.com/en/dashboard/developers <br/>

Then set them into the `signature.py`. 
<br/>

There are 2 methods available in the code for testing: <br/>
- `query_order`
- `create_order`

Please feel free to add your own method to experience more endpoints.

```bash
python merchant.py
```

## Verifying Signature from webhook notifications

### Setting up the webhook

1. Ensure that you have a publicly accessible URL.
2. Set the publicly accessible URL as the webhook via the dashboard for binance pay here: https://merchant.binance.com/en/dashboard/developers
<br> Note: Webhook can only receive order result notifications for now. 
3. The path of the URL setup on the dashboard should be `/notify`
<br> eg. `https://public-address.me/notify`

### How to run

Install the dependencies and run `webhook.py`. Running `webhook.py` will start the flask server at port 5000 by default.

```bash
pip install -r requirements-webhook.txt
python webhook.py
```

The details about how verification is done can be found in the documentation here: https://developers.binance.com/docs/binance-pay/webhook-common

