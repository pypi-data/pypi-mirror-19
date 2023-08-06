# -*- coding:utf8 -*-

from __future__ import absolute_import
import sys
from .client.utils import VERSION

__version__ = VERSION


if (2, 7) <= sys.version_info < (3, 2):
    # On Python 2.7 and Python3 < 3.2, install no-op handler to silence
    # `No handlers could be found for logger "stream"` message per
    # <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
    import logging
    logger = logging.getLogger('stream')
    logger.addHandler(logging.NullHandler())
