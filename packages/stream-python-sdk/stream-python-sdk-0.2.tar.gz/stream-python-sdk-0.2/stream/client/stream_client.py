# -*- coding:utf8 -*-

from .utils import HTTP_METHOD
from ..transport import Transport
from ..exceptions import InvalidParameter
from .properties import (LOG_SUBSCRIPTION_HOST, GET_LOG_RESOURCE_PATH,
                         SUBSCRIPTION_POSITION_RESOURCE_PATH)

class StreamClient(object):
    """
    The client for accessing the Netease Stream service.
    """

    def __init__(self, access_key_id=None, access_key_secret=None,
                 transport_class=Transport, **kwargs):
        """
        The parameter of 'access_key_id' or 'access_key_secret' should be
        given by string.

        Args:
            access_key_id(string): The access key ID. 'None' is set by default.
            access_key_secret(string): The secret access key. 'None' is set by
                default.
            transport_class(class): The class will be used for
                transport. 'stream.transport.Transport' is set by default.
            kwargs: Other optional parameters.
        """
        self.transport = transport_class(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            **kwargs
        )

    def get_subscription_position(self, subscription_name, position_type, **kwargs):
        """
        Get subscription position.

        Args:
            subscription_name(string): subscription logs name.
            position_type(string): wanted log position type.
            kwargs: Other optional parameters.

        Returns:
            return_value(string): The response of Stream server.
        """
        if subscription_name is not None and subscription_name == '':
            raise InvalidParameter('subscription_name')

        if position_type is not None and position_type == '':
            raise InvalidParameter('position_type')

        headers = dict()
        body = dict()
        body['position_type'] = position_type
        response = self.transport.perform_request(
            method=HTTP_METHOD.POST, topic_name=subscription_name,
            end_point=LOG_SUBSCRIPTION_HOST,
            resource_path=SUBSCRIPTION_POSITION_RESOURCE_PATH,
            body=body, headers=headers
        )

        return response

    def get_logs(self, subscription_name, logs_position, limit, **kwargs):
        """
        Get subscription logs.

        Args:
            subscription_name(string): subscription logs name.
            logs_position(string): wanted log position type.
            limit(int): number of records to get
            kwargs: Other optional parameters.

        Returns:
            return_value(string): The response of Stream server.
        """
        if subscription_name is not None and subscription_name == '':
            raise InvalidParameter('subscription_name')
        if logs_position is not None and logs_position == '':
            raise InvalidParameter('logs_position')
        if limit is not None and limit < 1:
            raise InvalidParameter('limit')

        headers = dict()
        body = dict()
        body['position'] = logs_position
        body['limit'] = limit
        response = self.transport.perform_request(
            method=HTTP_METHOD.POST, topic_name=subscription_name,
            end_point=LOG_SUBSCRIPTION_HOST,
            resource_path=GET_LOG_RESOURCE_PATH,
            body=body, headers=headers
        )

        return response