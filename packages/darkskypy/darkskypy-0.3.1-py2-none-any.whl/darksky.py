# -*- coding: utf-8 -*-
"""
This is the core module, recieves the api key, latitude, longitude,
and optional parameters. It builds the request url, makes a HTTP request
to recieves a utf-8-encoded, JSON-formmated object.
"""

import sys
import os
import requests
import requests.exceptions
from attrdict import AttrDict

#TODO
#Need to add error catching for bad latlng or missing variables
#Better DocString

class DarkSky(object):
    """
    Requires that an API key has been set somewhere or is provided.
    Also need to include the longitude and latitude for the location.

    Some attributes of DarkSky:
    self.url        - the full request url
    self.json       - json decoded output equivalent to json.loads(...)
    self.header     - dict of the HTTP Header
    self.forecast   - attrdict object


    """

    base_url = 'https://api.darksky.net/forecast/'

    def __init__(self, location, **kwargs):
        """
        """
        # the api_key should be stored as an os.environment
        API_KEY = os.environ.get('DARKSKY_API_KEY')

        self.latitude = location[0]
        self.longitude = location[1]
        self.api_key = API_KEY if API_KEY else kwargs.get('apikey', None)
        if self.api_key is None:
            raise KeyError('Missing API Key. DarkSky(location, apikey=...')

    # See, https://darksky.net/dev/docs/forecast
    # for optional request parameters
        self.params = {
            'exclude': kwargs.get('exclude', None),
            'extend': kwargs.get('extend', None),
            'lang': kwargs.get('lang', 'en'),
            'units': kwargs.get('units', 'auto'),
        }

        self.get_forecast(
            self.base_url,
            apikey=self.api_key,
            latitude=self.latitude,
            longitude=self.longitude,
            params=self.params,
        )

    def get_forecast(self, base_url, **kwargs):
        try:
            reply = self._connect(base_url, **kwargs)
        except:
            raise

        self.forecast = AttrDict(reply)

    def _connect(self, base_url, **kwargs):
        """
        builds request url and makes an HTTP request.
        Returns the JSON decoded object.

        If network problem raises request exceptions
        (Timeout, ConnectionError, HTTPError, etc)
        Darksy.net will raise a 404 error if latitude or longitude are missing
        """
        head = {'Accept-Encoding': 'gzip, deflate'}
        url = base_url + '{apikey}/{latitude},{longitude}'.format(**kwargs)

        try:
            r = requests.get(url, headers=head, params=self.params, timeout=20)
            r.raise_for_status()
        except HTTPError:
            raise
        except RequestException as error:
            print(error)
            raise
        try:
            self.json = r.json()
        except ValueError:
            raise
        # HTTP response headers see https://darksky.net/dev/docs/response
        self.headers = r.headers
        self.url = r.url

        return self.json
