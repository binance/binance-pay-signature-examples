import hmac
import uuid
import json
import time
import logging
import hashlib
import requests

""" This is a very simple script working on Binance Pay API

Set your KEY and SECRET, then you are ready to go.

```python

python main.py

```

"""

logging.basicConfig(level=logging.DEBUG)

KEY = ''
SECRET = ''
BASE_URL = 'https://bpay.binanceapi.com'

''' ======  begin of functions, you don't need to touch ====== '''
def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha512).hexdigest().upper()

def get_timestamp():
    return int(time.time() * 1000)

def random_string():
    random = str(uuid.uuid4())
    random = random.replace("-","") 
    return random[0:32]

def dispatch_request(http_method, header):
    session = requests.Session()
    session.headers.update({
        'content-type': 'application/json',
        'BinancePay-Timestamp': header['timestamp'],
        'BinancePay-Nonce': header['nonce'],
        'BinancePay-Certificate-SN': header['api_key'],
        'BinancePay-Signature': header['signature']
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')

# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):

    timestamp = get_timestamp()
    nonce = random_string()
    payload_to_sign = str(timestamp) + "\n" + nonce + "\n" + json.dumps(payload) + "\n"
    url = BASE_URL + url_path
    signature = hashing(payload_to_sign)
    header = {
      "timestamp": str(timestamp),
      "nonce": nonce,
      "api_key": KEY,
      "signature": signature
    }
    params = {"url": url, "data": json.dumps(payload) }
    response = dispatch_request(http_method, header)(**params)
    return response.json()
    
''' ======  end of functions ====== '''


# Query Order
# 
# POST /binancepay/openapi/order/query
# https://developers.binance.com/docs/binance-pay/api-order-query
def query_order():
  response = send_signed_request(
    'POST', 
    '/binancepay/openapi/order/query',
    {
      'merchantId': '123456789',
      'merchantTradeNo': '121055692278489088'
    }
  )
  print(response)

query_order()


# Create Order
# 
# POST /binancepay/openapi/order
# https://developers.binance.com/docs/binance-pay/api-order-create
def create_order():
  response = send_signed_request(
    'POST', 
    '/binancepay/openapi/order',
    {
      'merchantId': '123456789',
      'merchantTradeNo': '123',
      'tradeType': 'WEB',
      'totalFee': '0.01',
      'currency': 'USDT',
      'productType': 'fruit',
      'productName': 'apple juice',
      'productDetail': 'juicy apple juice'
    }
  )
  print(response)

create_order()

# You are free to test on more endpoint with send_signed_request
# https://developers.binance.com/docs/binance-pay/api-order-create
