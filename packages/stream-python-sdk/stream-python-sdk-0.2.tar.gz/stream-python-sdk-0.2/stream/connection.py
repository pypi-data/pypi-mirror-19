# -*- coding:utf8 -*-

import certifi
import urllib3
from urllib3.exceptions import ReadTimeoutError

from .exceptions import (ConnectionError, ConnectionTimeout)

class Urllib3HttpConnection(object):

    def __init__(self, num_pools=16, enable_ssl=False, **kwargs):
        if enable_ssl:
            self.pool = urllib3.PoolManager(num_pools=num_pools,
                                            cert_reqs='CERT_REQUIRED',
                                            ca_certs=certifi.where())
        else:
            self.pool = urllib3.PoolManager(num_pools=num_pools)

    def perform_request(self, method, url, body=None, headers={}, timeout=5):
        """ Perform request.

        Perform request with urllib3.

        Args:
            method: Post, put, etc.
            url: Where request be sended.
            body: Data to send.
            headers: Headers to send.
            timeout: Timeout for connection.

        Returns:
            status: Response.status.
            reason: Response.reason.
            data: Response.data.

        Raises:
            ConnectionTimeout: Connection timeout.
            ConnectionError: Connection error.
        """
        try:
            kw = {}
            if timeout:
                kw['timeout'] = timeout

            # in python2 we need to make sure the url and method are not
            # unicode. Otherwise the body will be decoded into unicode too and
            # that will fail.
            if not isinstance(url, str):
                url = url.encode('utf-8')
            if not isinstance(method, str):
                method = method.encode('utf-8')

            response = self.pool.urlopen(method, url, body=body, retries=False,
                                         headers=headers, **kw)
            return response.status, response.reason, response.data
        except ReadTimeoutError as e:
            raise ConnectionTimeout(str(e), e)
        except Exception as e:
            raise ConnectionError(str(e), e)
