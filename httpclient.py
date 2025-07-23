# -*- coding:utf-8 -*-

from http.client import HTTPSConnection, HTTPConnection, RemoteDisconnected
from urllib import parse
import ssl, json

HTTP_METHOD_GET = "GET"
HTTP_METHOD_PUT = "PUT"
HTTP_METHOD_POST = "POST"
HTTP_METHOD_DELETE = "DELETE"

def convertObj2Json(obj):
    return obj.__dict__

#将json对象序列化为字符串
def dumpJsonObjectToString(obj, convfunc=convertObj2Json, indent=None, sort_keys=False):
    result = ""
    try:
        result = json.dumps(obj, default=convfunc, indent=indent, sort_keys=sort_keys)
    except:
        print("dump json object catch an exception.")
    return result

class HTTPClient(object):
    def __init__(self, server_addr):
        parse_result = parse.urlparse(server_addr)
        scheme = parse_result.scheme
        host = parse_result.hostname
        port = parse_result.port
        if not port: port = 80 if scheme == "http" else 443
        if scheme == "http":
            self.connection = HTTPConnection(host, port)
        else:
            sslctx = ssl.create_default_context()
            sslctx.check_hostname = False
            sslctx.verify_mode = ssl.CERT_NONE
            self.connection = HTTPSConnection(host, port, context=sslctx)

    def get(self, url, headers):
        if headers is None: headers = {}
        return self.do(HTTP_METHOD_GET, url, None, headers, logger)

    def delete(self, url, headers):
        if headers is None: headers = {}
        return self.do(HTTP_METHOD_DELETE, url, None, headers, logger)

    def put(self, url, headers, obj, logger):
        if headers is None: headers = {}
        payload = None
        if obj is not None:
            try:
                payload = dumpJsonObjectToString(obj)
                headers["Content-Type"] = "application/json"
            except:
                logger.exception("json marshalling failure.")
        else:
            headers["Content-Type"] = "application/json"

        return self.do(HTTP_METHOD_PUT, url, payload, headers, logger)

    def post(self, url, headers, obj, logger):
        if headers is None: headers = {}
        payload = None
        if obj is not None:
            try:
                payload = dumpJsonObjectToString(obj)
                headers["Content-Type"] = "application/json"
            except:
                logger.exception("json marshalling failure.")
        else:
            headers["Content-Type"] = "application/json"

        return self.do(HTTP_METHOD_POST, url, payload, headers, logger)

    def do(self, method, url, payload, headers, logger):
        count = 0
        while count < 3:
            try:
                self.connection.request(method, url, payload, headers)
                response = self.connection.getresponse()
                status = response.status
                headers = response.getheaders()
                result = response.read()
                return status, headers, result
            except RemoteDisconnected as e:
                logger.error("request '%s' failed for remote connection closed(err: %s), will retry.", url, e)
                count += 1
            except:
                logger.exception("request '%s' failed.", url)
                return 0, None, None
