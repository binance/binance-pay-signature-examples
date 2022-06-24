from flask import Flask, request, jsonify, make_response
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode

from python.signature import send_signed_request

app = Flask(__name__)


@app.route('/')
def start():
    return 'Webhooks with Python'


@app.route('/notify', methods=['POST'])
def webhook_notification():
    print('Received Webhook Notification!')
    verify_signature(request.headers, request.data)
    data = {'message': 'Done', 'code': 'SUCCESS'}
    return make_response(jsonify(data), 200)


def get_pub_key():
    response = send_signed_request(
        'POST',
        '/binancepay/openapi/certificates',
    )
    return response['data'][0]['certPublic']


def verify_signature(headers, data):
    print('Verifying Signature...')
    print(headers)
    print(data)
    timestamp, nonce, signature = headers['Binancepay-Timestamp'], headers['Binancepay-Nonce'], headers[
        'Binancepay-Signature']
    payload = timestamp + '\n' + nonce + '\n' + data.decode('utf-8') + '\n'
    pub_key = get_pub_key()
    rsakey = RSA.importKey(pub_key)
    signer = PKCS1_v1_5.new(rsakey)
    digest = SHA256.new()
    digest.update(payload.encode('utf-8'))
    if signer.verify(digest, b64decode(signature)):
        print('Signature Verified!')
        return
    print("Signature Not Verified!")
    return


if __name__ == '__main__':
    app.run(debug=True)
