# -*- coding: utf-8 -*-

"""
OAuth2 Class supporting client credential token grants.
"""


import requests
from urllib import quote, urlencode
from urlparse import parse_qs
try:
    import simplejson as json
except ImportError:
    import json
import base64
import tkMessageBox
from login_frame import LoginFrame

import sys
sys.path.append('C:/Users/Andrew/Desktop/bcbstore/POSSystem/')
from SharedUtilities import printt


class OAuth2(object):
    authorization_url = '/oauth/authorize'
    token_url = '/oauth/token'

    def __init__(self, client_id, client_secret, site, redirect_uri, authorization_url=None, token_url=None):
        """
        Initializes the hook with OAuth2 parameters
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.site = site
        self.redirect_uri = redirect_uri
        if authorization_url is not None:
            self.authorization_url = authorization_url
        if token_url is not None:
            self.token_url = token_url

    def authorize_url(self, scope='', **kwargs):
        """
        Returns the url to redirect the user to for user consent
        """
        oauth_params = {'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'scope': scope}
        oauth_params.update(kwargs)
        return "%s%s?%s" % (self.site, quote(self.authorization_url), urlencode(oauth_params))

    def get_token(self, code, **kwargs):
        """
        Requests an access token
        """
        url = "%s%s" % (self.site, quote(self.token_url))
        data = {'redirect_uri': self.redirect_uri, 'client_id': self.client_id, 'client_secret': self.client_secret, 'code': code}
        data.update(kwargs)
        response = requests.post(url, data=data)

        if isinstance(response.content, basestring):
            try:
                content = json.loads(response.content)
            except ValueError:
                content = parse_qs(response.content)
        else:
            content = response.content

        return content

    def request_grant_token(self, username, password, consumer_key=False, consumer_secret=False):
        base64string = base64.encodestring('%s:%s' % (self.client_id, self.client_secret)).replace('\n', '')
        headers = {
            "Authorization": "Basic %s" % base64string,
            "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "BCBS Wordpress API Client-Python, oauth2",
            "accept": "application/json"
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': username,
            'password': password,
            "grant_type": "password"
        }

        return requests.post(self.site + self.token_url, headers=headers, data=data)

    def request_auth_token(self, error_title=None):
        if not error_title:
            error_title = "Error Authenticating with the Server"

        frame = LoginFrame(width=600, height=325)
        client_creds = frame.get_user_info()

        response = self.request_grant_token(
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            username=client_creds[0],
            password=client_creds[1]
        )
        printt(response.status_code)

        if response.status_code in (403, 401):
            tkMessageBox.showerror(
                error_title,
                str("There was an issue while authenticating with the store! \n You've entered an incorrect username "
                    "or password. Please try again later. If the issue persists then please reset your store password."))
            return {}
        elif not self.is_json(response.text):
            tkMessageBox.showerror(
                error_title,
                str("There was an issue while authenticating with the store — the response returned from the server was"
                    "unexpected and authentication cannot continue.\nPlease try again later. If the issue persists,"
                    " contact: webmaster@bcbud.store for assistance."))
            return {}
        elif not (response.status_code == 200):
            tkMessageBox.showerror(
                error_title,
                str("There was an unknown issue while authenticating with the store. This is likely caused by a "
                    "communications issue, and is (probably) not an issue with your password. Please try again in 10 "
                    "minutes, and if the issue persists contact: webmaster@bcbud.store for assistance.")
            )
            printt("There was an issue while authenticating with the store. Details: \n" + str(response.status_code))
            printt("Response that indicated an exception:")
            printt(response, pretty=True)
            return {}
        elif 'access_token' in response.json() and 'refresh_token' in response.json():
            return {
                response.json()['access_token'],
                response.json()['refresh_token']
            }

    def is_json(self, data):
        """
        Returns True if data is parseable JSON
        :param data:
        :return:
        """
        try:
            json_object = json.loads(data)
        except ValueError, e:
            return False
        return True
