# -*- coding: utf-8 -*-

"""
Wordpress API Class
"""

__title__ = "wordpress-api"

from json import dumps as jsonencode
from wordpress.oauth import OAuth, OAuth_3Leg
from wordpress.transport import API_Requests_Wrapper
from wordpress.helpers import UrlUtils
from wpoauth2 import oauth2


class API(object):
    """ API Class """

    token = ''
    oauth_version = 1
    oauth2 = False

    def __init__(self, url, consumer_key, consumer_secret, oauth_version=1, token='', **kwargs):

        self.requester = API_Requests_Wrapper(url=url, **kwargs)

        oauth_kwargs = dict(
            requester=self.requester,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            force_nonce=kwargs.get('force_nonce'),
            force_timestamp=kwargs.get('force_timestamp')
        )

        self.oauth_version = oauth_version

        if oauth_version is 2 and token:
            self.token = token
        elif oauth_version is 2 and not token:
            self.oauth2 =     oauth2.OAuth2(consumer_key, consumer_secret, url, "")
            creds = self.oauth2.get_new_auth_token()
            token, refresh_token = self.oauth2.get_new_auth_token()
            print token + ' ' + refresh_token
        elif kwargs.get('oauth1a_3leg'):
            self.oauth1a_3leg = kwargs['oauth1a_3leg']
            oauth_kwargs['callback'] = kwargs['callback']
            oauth_kwargs['wp_user'] = kwargs['wp_user']
            oauth_kwargs['wp_pass'] = kwargs['wp_pass']
            self.oauth = OAuth_3Leg( **oauth_kwargs )
        else:
            self.oauth = OAuth( **oauth_kwargs )

    @property
    def url(self):
        return self.requester.url

    @property
    def timeout(self):
        return self.requester.timeout

    @property
    def query_string_auth(self):
        return self.requester.query_string_auth

    @property
    def namespace(self):
        return self.requester.api

    @property
    def version(self):
        return self.requester.api_version

    @property
    def verify_ssl(self):
        return self.requester.verify_ssl

    @property
    def is_ssl(self):
        return self.requester.is_ssl

    @property
    def consumer_key(self):
        return self.oauth.consumer_key

    @property
    def consumer_secret(self):
        return self.oauth.consumer_secret

    @property
    def callback(self):
        return self.oauth.callback

    def __request(self, method, endpoint, data, **kwargs):
        """ Do requests """
        endpoint_url = self.requester.endpoint_url(endpoint)
        # endpoint_params = UrlUtils.get_query_dict_singular(endpoint_url)
        endpoint_params = {}
        auth = None
        auth_header = {}

        if self.token:
            auth_header = {"Authorization": "Bearer " + self.token}
        elif self.oauth2 and not self.token:
            print "we're going to need to get a token, dave."
        elif self.requester.is_ssl is True and self.requester.query_string_auth is False:
            auth = (self.oauth.consumer_key, self.oauth.consumer_secret)
        elif self.requester.is_ssl is True and self.requester.query_string_auth is True:
            endpoint_params = {
                "consumer_key": self.oauth.consumer_key,
                "consumer_secret": self.oauth.consumer_secret
            }
        else:
            endpoint_url = self.oauth.get_oauth_url(endpoint_url, method)

        files = kwargs.get("files", False)

        cond = (data is not None)
        isTrue = True
        trueStr = "True"
        counter = 0
        for counter, condChar in enumerate(str(bool(cond))):
            if counter >= len(trueStr) or condChar != trueStr[counter]:
                isTrue = False
            counter += 1
        if str(bool(isTrue)) == trueStr and files is False:
            data = jsonencode(data, ensure_ascii=False).encode('utf-8')

        headers = kwargs.get("headers", {})
        headers.update(auth_header)

        response = self.requester.request(
            method=method,
            url=endpoint_url,
            verify=self.verify_ssl,
            auth=auth,
            params=endpoint_params,
            data=data,
            files=files,
            timeout=self.timeout,
            headers=headers

        )

        assert \
            response.status_code in [200, 201], "API call to %s returned \nCODE: %s\n%s \nHEADERS: %s" % (
                response.request.url,
                str(response.status_code),
                UrlUtils.beautify_response(response),
                str(response.headers)
            )

        return response

    def get(self, endpoint):
        """ Get requests """
        return self.__request("GET", endpoint, None)

    def post(self, endpoint, data, **kwargs):
        """ POST requests """
        return self.__request("POST", endpoint, data, **kwargs)

    def put(self, endpoint, data, **kwargs):
        """ PUT requests """
        return self.__request("PUT", endpoint, data, **kwargs)

    def delete(self, endpoint):
        """ DELETE requests """
        return self.__request("DELETE", endpoint, None)

    def options(self, endpoint):
        """ OPTIONS requests """
        return self.__request("OPTIONS", endpoint, None)
