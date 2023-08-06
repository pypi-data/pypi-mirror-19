# -*- coding: utf-8 -*-
import time
import json
import hmac
import hashlib
import inspect
import cerberus
from datetime import datetime
from abc import ABCMeta, abstractmethod
from websocket import create_connection
from future.moves.urllib.parse import urlencode
from zaifapi.api_common import get_response

SCHEMA = {
    'from_num': {
        'type': 'integer'
    },
    'count': {
        'type': 'integer'
    },
    'from_id': {
        'type': 'integer'
    },
    'end_id': {
        'type': ['string', 'integer']
    },
    'order': {
        'type': 'string',
        'allowed': ['ASC', 'DESC']
    },
    'since': {
        'type': 'integer'
    },
    'end': {
        'type': ['string', 'integer']
    },
    'currency_pair': {
        'type': 'string',
        'allowed': ['btc_jpy', 'xem_jpy', 'mona_jpy', 'mona_btc']
    },
    'currency': {
        'required': True,
        'type': 'string',
        'allowed': ['jpy', 'btc', 'mona']
    },
    'address': {
        'required': True,
        'type': 'string'
    },
    'message': {
        'type': 'string'
    },
    'amount': {
        'required': True,
        'type': 'number'
    },
    'opt_fee': {
        'type': 'number'
    },
    'order_id': {
        'required': True,
        'type': 'integer'
    },
    'action': {
        'required': True,
        'type': 'string',
        'allowed': ['bid', 'ask']
    },
    'price': {
        'required': True,
        'type': 'number'
    },
    'limit': {
        'type': 'number'
    }
}


class AbsZaifApi(object):
    __metaclass__ = ABCMeta
    _api_domain = 'api.zaif.jp'

    def params_pre_processing(self, schema_keys, params):
        schema = self.__get_schema(schema_keys)
        self.__validate(schema, params)
        return self.__edit_params(params)

    @classmethod
    def __get_schema(cls, keys):
        schema = {}
        for key in keys:
            schema[key] = SCHEMA[key]
        return schema

    @classmethod
    def __edit_params(cls, params):
        if 'from_num' in params:
            params['from'] = params['from_num']
            del (params['from_num'])
        return params

    @classmethod
    def __validate(cls, schema, param):
        v = cerberus.Validator(schema)
        if v.validate(param):
            return
        raise Exception(json.dumps(v.errors))


class ZaifPublicApi(AbsZaifApi):
    __API_URL = 'https://{}/api/1/{}/{}'

    def __params_pre_processing(self, currency_pair):
        params = {
            'currency_pair': currency_pair
        }
        super(ZaifPublicApi, self).params_pre_processing(['currency_pair'], params)

    def __execute_api(self, func_name, currency_pair):
        self.__params_pre_processing(currency_pair)
        return get_response(self.__API_URL.format(self._api_domain, func_name, currency_pair))

    def last_price(self, currency_pair):
        return self.__execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def ticker(self, currency_pair):
        return self.__execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def trades(self, currency_pair):
        return self.__execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def depth(self, currency_pair):
        return self.__execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def streaming(self, currency_pair):
        self.__params_pre_processing(currency_pair)
        ws = create_connection('ws://api.zaif.jp:8888/stream?currency_pair={}'.format(currency_pair))
        result = ws.recv()
        ws.close()
        return json.loads(result)


class AbsZaifPrivateApi(AbsZaifApi):
    __API_URL = 'https://{}/tapi'

    @abstractmethod
    def get_header(self, params):
        raise NotImplementedError()

    @classmethod
    def __get_parameter(cls, func_name, params):
        params['method'] = func_name
        params['nonce'] = int(time.mktime(datetime.now().timetuple()))
        return urlencode(params)

    def __execute_api(self, func_name, schema_keys=None, params=None):
        if schema_keys is None:
            schema_keys = []
        if params is None:
            params = {}
        params = self.params_pre_processing(schema_keys, params)
        params = self.__get_parameter(func_name, params)
        header = self.get_header(params)
        res = get_response(self.__API_URL.format(self._api_domain), params, header)
        if res['success'] == 0:
            raise Exception(res['error'])
        return res['return']

    def get_info(self):
        return self.__execute_api(inspect.currentframe().f_code.co_name)

    def get_info2(self):
        return self.__execute_api(inspect.currentframe().f_code.co_name)

    def get_personal_info(self):
        return self.__execute_api(inspect.currentframe().f_code.co_name)

    def trade_history(self, **kwargs):
        schema_keys = ['from_num', 'count', 'from_id', 'end_id', 'order', 'since', 'end', 'currency_pair']
        return self.__execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def active_orders(self, **kwargs):
        schema_keys = ['currency_pair']
        return self.__execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def __inner_history_api(self, func_name, kwargs):
        schema_keys = ['currency', 'from_num', 'count', 'from_id', 'end_id', 'order', 'since', 'end']
        return self.__execute_api(func_name, schema_keys, kwargs)

    def withdraw_history(self, **kwargs):
        return self.__inner_history_api(inspect.currentframe().f_code.co_name, kwargs)

    def deposit_history(self, **kwargs):
        return self.__inner_history_api(inspect.currentframe().f_code.co_name, kwargs)

    def withdraw(self, **kwargs):
        schema_keys = ['currency', 'address', 'message', 'amount', 'opt_fee']
        return self.__execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def cancel_order(self, **kwargs):
        schema_keys = ['order_id']
        return self.__execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def trade(self, **kwargs):
        schema_keys = ['currency_pair', 'action', 'price', 'amount', 'limit']
        return self.__execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)


class ZaifPrivateApi(AbsZaifPrivateApi):
    def __init__(self, key, secret):
        self.__key = key
        self.__secret = secret
        super(ZaifPrivateApi, self).__init__()

    def get_header(self, params):
        signature = hmac.new(bytearray(self.__secret.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(params.encode('utf-8'))
        return {
            'key': self.__key,
            'sign': signature.hexdigest()
        }


class ZaifPrivateTokenApi(AbsZaifPrivateApi):
    def __init__(self, token):
        self.__token = token
        super(ZaifPrivateTokenApi, self).__init__()

    def get_header(self, params):
        return {
            'token': self.__token
        }
