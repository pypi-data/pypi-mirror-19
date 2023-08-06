# -*- coding:utf8 -*-

import json

from .connection import Urllib3HttpConnection
from .serializer import JSONSerializer
from .exceptions import StreamException
from .client.auth import RequestMetaData

class Transport(object):
    """
    Encapsulation of transport-related to logic. Handles instantiation of the
    individual connections as well as creating a connection pool to hold them.

    Main interface is the `perform_request` method.
    """

    def __init__(self, access_key_id=None, access_key_secret=None,
                 connection_class=Urllib3HttpConnection,
                 serializer=JSONSerializer(),
                 timeout=5, enable_ssl=False, **kwargs):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.timeout = timeout
        self.enable_ssl = enable_ssl
        self.serializer = serializer
        kwargs.setdefault('enable_ssl', self.enable_ssl)
        self.connection = connection_class(**kwargs)

    def perform_request(self, method, topic_name, end_point,
                        resource_path, body=None, headers={}, timeout=30):
        """ Perform request.
        
        Perform request with urllib3.
            
        Args:
            method: Post, put, etc.
            url: Where request be sended.
            body: Data to send.
            headers: Headers to send.
            timeout: Timeout for connection.
        
        Returns:
            response: Include status, reason and data.
        
        Raises:
            StreamException: stream exception.
        """
        method = method.encode('utf-8') \
            if isinstance(method, unicode) else method

        if body is not None:
            body = self.serializer.dumps(body)

        meta_data = RequestMetaData(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            method=method,
            topic_name=topic_name,
            end_point=end_point,
            resource_path=resource_path,
            body=body,
            headers=headers,
            enable_ssl=self.enable_ssl
        )

        url = meta_data.get_url()
        headers = meta_data.get_headers()
        try:
            status, reason, data = self.connection.perform_request(
                method, url, body, headers,
                timeout=(timeout or self.timeout)
            )
            return self.create_response(status, reason, data)
        except StreamException as e:
            raise Exception(e)

    def create_response(self, status, reason, data):
        """ Create response.
        
        Args:
            status: Response.status.
            reason: Response.reason.
            data: Response.data.
        
        Returns:
            response: Include status, reason and data.
        """
        response = {}
        response['code'] = status
        response['message'] = reason
        response['result'] = json.loads(data)
        return json.dumps(response)