from __future__ import (absolute_import, division, print_function, unicode_literals)
from future import standard_library  # noqa
from builtins import *  # noqa

import requests
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class LoginError(Exception):
    pass


class pyBNS(object):
    # Declare properties
    # Username and password are pulled from arguments given in instance.
    def __init__(self, *args, **kwargs):
        # go through keyword arguments
        for key, value in list(kwargs.items()):
            # if the keys are username and password, set self attributes
            if key in ['username', 'password']:
                setattr(self, key, value)
        # base url
        self.api_url = 'https://api.bloomberg.com/{0}'
        self.headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'authorization': 'Basic YkFSeWpFbGxWTGZHSmlYd2FlOFJpMHUzZVFRYTpKOVhDYmhiMG9zMFBPOGNEYUIwSlY5Z1JDMW9h'
        }

    def post(self, url, payload):
        url = self.api_url.format(url)
        # try posting the complete url, credentials and headers
        try:
            response = requests.post(url=url, data=payload, headers=self.headers)
            # raise an exception if it's not 200
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            status = response.status_code
            e.msg = 'Received a {0} response, instead of 200'.format(status)
            print(e.msg)

    def connect(self):
        # If there's not a username and password, raise an exception
        try:
            # quote username and password to get the special url encoding
            username = quote(self.username)
            password = quote(self.password)
        except AttributeError:
            msg = 'pybBNS instance requires a username and password'
            raise LoginError(msg)

        login_data = 'username={0}&password={1}&remember=false&grant_type=password'.format(username, password)
        # pass through url ending and payload
        response = self.post('syndication/token', login_data)
        # save access token for later use
        self.access_token = str(response.json()['access_token'])

    def disconnect(self):
        try:
            payload = 'token={0}'.format(self.access_token)
            # post token to api
            self.post('syndication/revoke', payload)
        except AttributeError as e:
            print(e)


# Create an instance, passing arguments as keyword arguments
bb = pyBNS()

# post credentials and header to /syndication/token
bb.connect()
# request api token be revoked
bb.disconnect()