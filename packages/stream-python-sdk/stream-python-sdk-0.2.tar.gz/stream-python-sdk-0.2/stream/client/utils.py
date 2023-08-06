# -*- coding:utf8 -*-

import platform

def enum(**enums):
    return type('Enum', (), enums)

HTTP_METHOD = enum(
    HEAD='HEAD',
    GET='GET',
    POST='POST',
    PUT='PUT',
    DELETE='DELETE'
)

HTTP_HEADER = enum(
    AUTHORIZATION='Authorization',
    CONTENT_LENGTH='Content-Length',
    CONTENT_TYPE='Content-Type',
    CONTENT_MD5='Content-MD5',
    HOST='Host',
    DATE='Date',
    USER_AGENT='User-Agent',
)
VERSION = '0.2'
TIME_GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
USER_AGENT = 'stream-python-sdk/%s python%s %s' % (VERSION, platform.python_version(), ' '.join(platform.uname()))