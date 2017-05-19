# -*- coding: utf-8 -*-

"""
oauth2 barebones and helpers class
"""

class Oauth2(object):



    def __init__(self, api_uri, client_key, client_secret, access_token=False, refresh_token=False):
        self.api_uri = api_uri
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token

    @property
    def get_token(self):
        return self.client_key
