"""
Client for Distelli REST API
https://www.distelli.com/docs/api/
"""

import json
import os
from requests import Request, Session, ConnectionError, HTTPError


class DistelliException(Exception):
    pass


class Distelli(object):
    _endpoint = 'https://api.distelli.com/'

    def __init__(self, username=None, api_token=None):
        """
        Create authenticated API client.
        Provide `username` and `api_token`.
        """
        if username is None:
            username = os.getenv('DISTELLI_USERNAME')
        if api_token is None:
            api_token = os.getenv('DISTELLI_API_TOKEN')

        if username is None or api_token is None:
            raise DistelliException('No authentication details provided.')

        self.__username, self.__api_token = username, api_token

    def __rest_helper(self, url, data=None, params=None, method='GET'):
        """
        Handles requests to the Distelli API, defaults to GET requests if none
        provided.
        """

        url = "{endpoint}/{username}{url}?apiToken={api_token}".format(
            endpoint=self._endpoint,
            username=self.__username,
            url=url,
            api_token=self.__api_token,
        )
        headers = {
            'Content-Type': 'application/json'
        }

        request = Request(
            method=method,
            url=url,
            headers=headers,
            data=json.dumps(data),
            params=params,
        )

        prepared_request = request.prepare()

        result = self.__request_helper(prepared_request)

        return result

    @staticmethod
    def __request_helper(request):
        """Handles firing off requests and exception raising."""
        try:
            session = Session()
            handle = session.send(request)

        except ConnectionError:
            raise DistelliException('Failed to reach a server.')

        except HTTPError:  # pragma: no cover
            raise DistelliException('Invalid response.')

        response = handle.json() if handle.content else {}

        if 400 <= handle.status_code:
            raise DistelliException(response)

        return response

    # Apps

    def apps(self):
        """Get a list of all apps."""
        return self.__rest_helper('/apps', method='GET')['apps']

    def app(self, app_name):
        """Get the details for a specific app."""
        url = '/apps/{name}'.format(name=app_name)
        return self.__rest_helper(url, method='GET')['app']

    def create_app(self, app_name, description=''):
        """Create an application."""
        data = {'description': description}
        url = '/apps/{name}'.format(name=app_name)
        return self.__rest_helper(url, data, method='PUT')['app']

    def delete_app(self, app_name):
        """Delete an application."""
        url = '/apps/{name}'.format(name=app_name)
        return self.__rest_helper(url, method='DELETE')

    # Environments

    def envs(self):
        """Get a list of environments."""
        return self.__rest_helper('/envs', method='GET')['envs']

    def env(self, env_name):
        """Get the details for a specific environment."""
        url = '/envs/{name}'.format(name=env_name)
        return self.__rest_helper(url, method='GET')['env']

    def create_env(self, app_name, env_name, description=''):
        """Create an environment."""
        data = {'description': description}
        url = '/apps/{app_name}/envs/{env_name}'.format(
            app_name=app_name,
            env_name=env_name,
        )
        return self.__rest_helper(url, data, method='PUT')['env']

    def delete_env(self, env_name):
        """Delete an environment."""
        url = '/envs/{name}'.format(name=env_name)
        return self.__rest_helper(url, method='DELETE')

    def add_env_servers(self, env_name, servers):
        """Add servers to an application environment."""
        data = {
            'action': 'add',
            'servers': servers,
        }
        url = '/envs/{name}/servers'.format(name=env_name)
        return self.__rest_helper(url, data, method='PATCH')['servers']

    def remove_env_servers(self, env_name, servers):
        """Remove servers from an application environment."""
        data = {
            'action': 'remove',
            'servers': servers,
        }
        url = '/envs/{name}/servers'.format(name=env_name)
        return self.__rest_helper(url, data, method='PATCH')['servers']

    # Servers

    def servers(self):
        """Get a list of all servers."""
        return self.__rest_helper('/servers', method='GET')['servers']

    def server(self, server_id):
        """Get a view a specific server."""
        url = '/servers/{name}'.format(name=server_id)
        return self.__rest_helper(url, method='GET')['server']

    def delete_server(self, server_id):
        """Delete a server from your account."""
        url = '/servers/{name}'.format(name=server_id)
        return self.__rest_helper(url, method='DELETE')
