# Binance Pay API signature in Nodejs


## How to run

The code is written in Nodejs with minimual dependencies, `axios` and `crypto-js` are required.

```javascript

// install the packages
npm install

```

## Setup the API key and secret

The API key and secret are required for working on Binance Pay API. It can be generated from:
https://merchant.binance.com/en/dashboard/developers <br/>

Then set them into the `merchant.js`. 
<br/>
There are 2 methods available in the code for testing: <br/>
- `query_order`
- `create_order`

Please feel free to add your own method to experience more endpoints.

```python
node merchant.js
```
