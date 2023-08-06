# -*- coding:utf8 -*-

import base64
import hashlib
import hmac
import time
import copy

from .utils import (HTTP_HEADER, TIME_GMT_FORMAT,
                    USER_AGENT)

class RequestMetaData(object):
    """
    Used to generate authorization header  and request url
    """

    def __init__(self, access_key_id, access_key_secret, method,
                 topic_name, end_point,
                 resource_path, body=None,
                 headers={}, enable_ssl=False):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.method = method
        self.topic_name = topic_name
        self.end_point = end_point
        self.resource_path = resource_path
        self.headers = copy.deepcopy(headers)
        self.enable_ssl = enable_ssl
        self.body = body
        self.url = ''

        self._complete_headers()
        self._complete_url()

    def get_url(self):
        """ Get url."""
        return self.url

    def get_headers(self):
        """ Get headers."""
        return self.headers

    def _complete_headers(self):
        """ Set headers."""
        # init date header
        self.headers[HTTP_HEADER.DATE] = time.strftime(
            TIME_GMT_FORMAT, time.gmtime(time.time() + 8 * 3600)
        )

        self.headers[HTTP_HEADER.CONTENT_TYPE] = 'application/json'
        #self.headers[HTTP_HEADER.HOST] = '%s.%s' % (
        #    self.topic_name, self.end_point)

        # init user-agent header
        self.headers.setdefault(HTTP_HEADER.USER_AGENT, USER_AGENT)

        # init content-md5 header
        if self.body is not None:
            md5 = hashlib.md5()
            md5.update(self.body)
            md5sum = md5.hexdigest()
            self.headers[HTTP_HEADER.CONTENT_MD5] = md5sum

        # init authorization header
        if None not in (self.access_key_id, self.access_key_secret):
            str_to_sign = self._get_string_to_sign()
            hmac_sha1 = hmac.new(str(self.access_key_secret),
                                 str_to_sign, hashlib.sha256)
            b64_hmac_sha1 = base64.encodestring(hmac_sha1.digest()).strip()
            authorization_string = b64_hmac_sha1.rstrip('\n')

            self.headers[HTTP_HEADER.AUTHORIZATION] = 'LOG %s:%s' % (
                self.access_key_id, authorization_string
            )

    def _complete_url(self):
        """
        build the url

        Returns:
            url
        """
        self.url = "https://" if self.enable_ssl else "http://"
        if self.topic_name is not None:
            self.url += '%s.%s%s' % (self.topic_name, self.end_point, self._get_canonicalized_resource())
        else:
            self.url += '%s%s' % (self.end_point, self._get_canonicalized_resource())
        #self.url += '%s%s' % (self.end_point,
        #                       self._get_canonicalized_resource())

    def _get_string_to_sign(self):
        """
        Generate string which should be signed and setted in header while
        sending request.

        Returns:
            canonical string for netease storage service.
        """
        headers = dict([(k.lower(), str(v).strip().strip("'\""))
                        for k, v in self.headers.iteritems()])

        content_type = headers.get(HTTP_HEADER.CONTENT_TYPE.lower(), '')
        content_md5 = headers.get(HTTP_HEADER.CONTENT_MD5.lower(), '')
        date = headers.get(HTTP_HEADER.DATE.lower(), '')

        # compute string to sign
        str_to_sign = '%s\n%s\n%s\n%s\n' % (
            self.method,
            content_md5,
            content_type,
            date
        )

        str_to_sign += "\n%s" % (self._get_canonicalized_resource())
        return str_to_sign

    def _get_canonicalized_resource(self):
        """
        Get canoicalized resource.
        
        Returns:
            get canoicalized resource.
        """

        return self.resource_path
