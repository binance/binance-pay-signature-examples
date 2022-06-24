
import logging

from python.signature import send_signed_request

""" This is a very simple script working on Binance Pay API

Set your KEY and SECRET in signature.py, then you are ready to go.

"""

logging.basicConfig(level=logging.DEBUG)

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

# You are free to test on more endpoints with send_signed_request
# https://developers.binance.com/docs/binance-pay/api-order-create
