"""
Send HTTP requests to the Norad HTTP API.
"""
import requests

from norad.models import Organization, Machine


class Client(object):
    """ A client for Norad's HTTP API.
    """

    # The default base URL for Norad's API
    DEFAULT_API_URL = 'https://norad.cisco.com:8443'

    # The default API version for Norad's API
    DEFAULT_API_VERSION = 'v1'

    def __init__(self, token, base_url=None):
        """ Set up an HTTP client for Norad.

        `token` is a user API token.
        `base_url` is the Norad API server's URL (including the version).
        """
        norad_url = base_url or '{api_url}/{version}/'.format(
            api_url=self.DEFAULT_API_URL,
            version=self.DEFAULT_API_VERSION
        )
        self.http = HttpHelper(token, norad_url)

    def all_organizations(self):
        """ List all organizations.
        """
        path = 'organizations'
        organizations = self.http.get(path)
        return [Organization(self.http, **info) for info in organizations]

    def organization(self, name):
        """ Get an organization by ID.
        """
        return Organization(self.http, uid=name)

    def machine(self, name):
        """ Get a machine by ID.
        """
        return Machine(self.http, id=name)


class HttpHelper(object):
    """ A helper class for sending HTTP requests to Norad.

    The current design involves passing one instance around the application.
    """

    def __init__(self, token, base_url):
        self.base_url = base_url
        self.auth_header = 'Token token={token}'.format(token=token)

    def get(self, path):
        """ Send an HTTP GET request to Norad.
        """
        return self.request('get', path)

    def post(self, path, data=None):
        """ Send an HTTP POST request to Norad.
        """
        return self.request('post', path, data=data)

    def put(self, path, data=None):
        """ Send an HTTP PUT request to Norad.
        """
        return self.request('put', path, data=data)

    def delete(self, path):
        """ Send an HTTP DELETE request to Norad.
        """
        return self.request('delete', path)

    def request(self, method, path, data=None):
        """ Send any HTTP request to Norad.

        For common cases, use methods like `self.get` and `self.post`.
        """
        url = self.base_url + path
        headers = {'Authorization': self.auth_header}
        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['response'] if response.content else None

