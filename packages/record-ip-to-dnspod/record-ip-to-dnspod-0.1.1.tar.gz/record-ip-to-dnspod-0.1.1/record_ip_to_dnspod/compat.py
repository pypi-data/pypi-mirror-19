# -*- coding: utf-8 -*-
import sys

PY2 = sys.version_info[0] == 2


if not PY2:
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    from configparser import ConfigParser
    is_str = lambda x: isinstance(x, basestring)  # noqa
else:
    from urllib import urlencode
    from urllib2 import urlopen, Request
    from ConfigParser import ConfigParser
    is_str = lambda x: isinstance(x, str)  # noqa


__all__ = ['urlencode', 'urlopen', 'Request', 'ConfigParser', 'is_str']
