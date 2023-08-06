import json
import httplib2
from pybagel import BagelExceptions


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class MoBagelClient(Singleton):
    def __init__(self, product_key=None, device_key=None, host="https://api.mobagel.com/v2"):
        self.http_client = httplib2.Http()
        self.product_key = product_key
        self.device_key = device_key
        self.host = host

    def setProductKey(self, product_key):
        self.product_key = product_key

    def setDeviceKey(self, device_key):
        self.device_key = device_key

    def setHost(self, host):
        self.host = host

    def registerDevice(self, content):
        headers = {
            'Product-Key': self.product_key,
            'Content-Type': "application/json"
        }
        url = self.host + "/register"
        _response, _content = self.http_client.request(url, 'POST', headers=headers, body=json.dumps(content))
        if int(int(_response['status'])/100) != 2:
            raise BagelExceptions.HttpsResponseException("Error: ", _response, _content)
        return _response['status'], _content

    def sendReport(self, content):
        headers = {
            'Device-Key': self.device_key,
            'Content-Type': "application/json"
        }
        url = self.host + "/report"
        _response, _content = self.http_client.request(url, 'POST', headers=headers, body=json.dumps(content))
        # Check Response 201:
        if int(int(_response['status'])/100) != 2:
            raise BagelExceptions.HttpsResponseException("Response Status Not 201", _response, _content)
        return _response['status'], _content
