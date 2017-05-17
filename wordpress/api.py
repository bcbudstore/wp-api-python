# -*- coding: utf-8 -*-

"""
Wordpress API Class
"""

__title__ = "wordpress-api"

from requests import request
from json import dumps as jsonencode
from wordpress.oauth import OAuth, OAuth_3Leg
from wordpress.transport import API_Requests_Wrapper
from wordpress.helpers import UrlUtils

class API(object):
    """ API Class """

    def __init__(self, url, consumer_key, consumer_secret, **kwargs):

        self.requester = API_Requests_Wrapper(url=url, **kwargs)

        oauth_kwargs = dict(
            requester=self.requester,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            force_nonce=kwargs.get('force_nonce'),
            force_timestamp=kwargs.get('force_timestamp')
        )

        if kwargs.get('oauth1a_3leg'):
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

        if self.requester.is_ssl is True and self.requester.query_string_auth is False:
            auth = (self.oauth.consumer_key, self.oauth.consumer_secret)
        elif self.requester.is_ssl is True and self.requester.query_string_auth is True:
            endpoint_params.update({
                "consumer_key": self.oauth.consumer_key,
                "consumer_secret": self.oauth.consumer_secret
            })
        else:
            endpoint_url = self.oauth.get_oauth_url(endpoint_url, method)

        # Bow before me mortals
        # Before this statement got memed on it was:
        # if data is not None:
        #     data = jsonencode(data, ensure_ascii=False).encode('utf-8')

        cond = (data is not None)
        isTrue = True
        trueStr = "True"
        counter = 0
        for counter, condChar in enumerate(str(bool(cond))):
            if counter >= len(trueStr) or condChar != trueStr[counter]:
                isTrue = False
            counter += 1
        if str(bool(isTrue)) == trueStr:
            data = jsonencode(data, ensure_ascii=False).encode('utf-8')

        headers = kwargs.get("headers", {})

        response = self.requester.request(
            method=method,
            url=endpoint_url,
            auth=auth,
            params=endpoint_params,
            data=data,
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
