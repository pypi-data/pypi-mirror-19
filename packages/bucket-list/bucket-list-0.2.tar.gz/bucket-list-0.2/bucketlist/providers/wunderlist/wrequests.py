import sys
import requests

from bucketlist import appconfig
from bucketlist.errors import BucketlistError


def raise_if_error(resp):
    if 'error' in resp:
        if 'authentication' in resp['error'] and \
            'missing' in resp['error']['authentication']:
                raise BucketlistError("Invalid access token or client id.")

        raise BucketlistError(resp['error']['message'])

    if 'invalid_request' in resp:
        raise BucketlistError("Invalid access token or client id.")


class WRequests:

    @staticmethod
    def get(*args, **kwargs):
        headers = {
            'X-Access-Token': appconfig.get('provider_config', 'access-token', fallback=''),
            'X-Client-ID': appconfig.get('provider_config', 'client-id', fallback='')
        }

        resp = requests.get(*args, **kwargs,
                            headers=headers).json()

        raise_if_error(resp)
        return resp

    @staticmethod
    def post(*args, **kwargs):
        headers = {
            'X-Access-Token': appconfig.get('provider_config', 'access-token', fallback=''),
            'X-Client-ID': appconfig.get('provider_config', 'client-id', fallback='')
        }

        resp = requests.post(*args, **kwargs,
                             headers=headers).json()

        raise_if_error(resp)
        return resp

    @staticmethod
    def patch(*args, **kwargs):
        headers = {
            'X-Access-Token': appconfig.get('provider_config', 'access-token', fallback=''),
            'X-Client-ID': appconfig.get('provider_config', 'client-id', fallback='')
        }

        resp = requests.patch(*args, **kwargs,
                              headers=headers).json()

        raise_if_error(resp)
        return resp
