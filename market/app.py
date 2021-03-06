"""
Market API
"""
import traceback
import json
from flask import Flask, jsonify, request
from service import MarketService
from settings import MARKET_URL


app = Flask(__name__, static_url_path='')


@app.route('/market', methods=['GET'])
def get_coins():
    """
    Returns coins from settings.market_url

    :statuscode 200: no error
    :statuscode 403: invalid creds
    """
    try:
        limit = request.args.get('limit', None)
        limit = int(limit) if limit else None
        market = MarketService().currentMarket(limit)
        return jsonify({'market': market.json()})
    except Exception, e:
        traceback.print_exc()


@app.before_request
def option_autoreply():
    """
    Always reply 200 on OPTIONS request
    """
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        resp_headers = resp.headers

        # Allow the origin which made the XHR
        resp_headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        resp_headers['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        resp_headers['Access-Control-Max-Age'] = "10"

        # keep current headers
        if headers is not None:
            resp_headers['Access-Control-Allow-Headers'] = headers
        return resp


@app.after_request
def set_allow_origin(resp):
    """
    Set origin for GET, POST, PUT, DELETE requests
    """
    resp_headers = resp.headers
    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        resp_headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    return resp
