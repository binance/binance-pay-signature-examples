const crypto = require('crypto');
const axios = require('axios');

// This is a very simple script working on Binance Pay API
// Set your apiKey and apiSecret, then you are ready to go.

const apiKey = '' // set your API key here 
const apiSecret = '' // set your secret key here
const baseURL = 'https://bpay.binanceapi.com'


// ===== functions ======

function hash_signature(query_string) {
  return crypto
      .createHmac('sha512', apiSecret)
      .update(query_string)
      .digest('hex');
}

function random_string() {
  return crypto.randomBytes(32).toString('hex').substring(0,32);
}

function dispatch_request(http_method, path, payload = {}) {
    const timestamp = Date.now()
    const nonce = random_string()
    const payload_to_sign = timestamp + "\n" + nonce + "\n" + JSON.stringify(payload) + "\n"
    const url = baseURL + path
    const signature = hash_signature(payload_to_sign)
    return axios.create({
      baseURL,
      headers: {
        'content-type': 'application/json',
        'BinancePay-Timestamp': timestamp,
        'BinancePay-Nonce': nonce,
        'BinancePay-Certificate-SN': apiKey,
        'BinancePay-Signature': signature.toUpperCase()
      }
    }).request({
      'method': http_method,
      url,
      data: payload
    })
}

// ===== functions ======


// Query Order
 
// POST /binancepay/openapi/order/query
// https://developers.binance.com/docs/binance-pay/api-order-query
function query_order() {
  dispatch_request(
    'POST', 
    '/binancepay/openapi/order/query',
    {
      'merchantId': '123456789',
      'merchantTradeNo': '121055692278489088'
    }
  ).then(response => console.log(response.data)).catch(error => console.log(error))
}

query_order()


// Create Order
//
// POST /binancepay/openapi/order
// https://developers.binance.com/docs/binance-pay/api-order-create
function create_order() {
  dispatch_request(
    'POST', 
    '/binancepay/openapi/order',
    {
      'merchantId': '123456789',
      'merchantTradeNo': '124',
      'tradeType': 'WEB',
      'totalFee': '0.01',
      'currency': 'USDT',
      'productType': 'fruit',
      'productName': 'apple juice',
      'productDetail': 'juicy apple juice'
    }
  ).then(response => console.log(response.data)).catch(error => console.log(error))
}

create_order()
