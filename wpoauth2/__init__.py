# -*- coding: utf-8 -*-

"""
wpoauth2
~~~~~~~~~
An oauth2 Python wrapper for token based authentication.
Also includes support for token retrieval and auth.

:copyright: modifications (c) 2017 by BCBud.store.
:license: MIT, see LICENSE for details.
"""

__title__ = "wpoauth2"
__version__ = "0.1"
__author__ = "BCBud.store, webmaster@bcbud.store"
__license__ = "MIT"

__default_api_version__ = "wp/v2"
__default_api__ = "wp-json"

from wpoauth2 import oauth2 as OAuth2
from wpoauth2 import login_frame as LoginFrame
