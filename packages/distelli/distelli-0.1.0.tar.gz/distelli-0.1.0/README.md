# Python Distelli

This is a client for the Distelli REST API. It currently allows you to fetch existing app info, as well as create and delete applications.

### Getting started

`distelli-python` depends on the `requests` library.

Install the library:

    pip install distelli

Import the module:

	from distelli import Distelli

Provide username and api\_token credentials:

    client = Distelli(username=YOUR_USERNAME, api_token=YOUR_API_TOKEN)

Or set environment variables:

    export DISTELLI_USERNAME=YOUR_USERNAME
    export DISTELLI_API_TOKEN=YOUR_API_TOKEN

Construct `Distelli` without any credentials:

    client = Distelli()

## Application operations

### View your existing applications:

Just run:

	apps = client.apps()

Results appear as a Python dict:

    [{'api_url': 'https://api.distelli.com/youraccount/apps/test_app',
      'builds_url': 'https://api.distelli.com/youraccount/apps/test_app/builds',
      'created': '2016-12-30T18:07:50.284Z',
      'deployments_url': 'https://api.distelli.com/youraccount/apps/test_app/deployments',
      'description': None,
      'html_url': 'https://www.distelli.com/youraccount/apps/test_app',
      'latest_build': None,
      'latest_release': None,
      'name': 'test_app',
      'owner': 'youraccount',
      'releases_url': 'https://api.distelli.com/youraccount/apps/test_app/releases'},
     {'api_url': 'https://api.distelli.com/youraccount/apps/test_app2',
      'builds_url': 'https://api.distelli.com/youraccount/apps/test_app2/builds',
      'created': '2016-12-30T18:24:07.511Z',
      'deployments_url': 'https://api.distelli.com/youraccount/apps/test_app2/deployments',
      'description': 'Another test app',
      'html_url': 'https://www.distelli.com/youraccount/apps/test_app2',
      'latest_build': None,
      'latest_release': None,
      'name': 'test_app2',
      'owner': 'youraccount',
      'releases_url': 'https://api.distelli.com/youraccount/apps/test_app2/releases'}]

### Get details for a specific application

	client.app('test_app2')

Results are the same as `apps()` above, but only show the app specified.

### Create an application

    client.create_app('test_app3', 'Description of the application')

Results are the same as `app()` above, but only show the app that was added.

### Delete an application

    client.delete_app('test_app3')

## Environments operations

### View your existing environments:

Just run:

	envs = client.envs()

Results appear as a Python dict:

    [{'active_release_url': 'https://api.distelli.com/youraccount/apps/demo-app/releases/v1',
      'active_release_version': 'v1',
      'api_url': 'https://api.distelli.com/youraccount/envs/demo-app-dev',
      'app_name': 'demo-app',
      'app_url': 'https://api.distelli.com/youraccount/apps/demo-app',
      'deployments_url': 'https://api.distelli.com/youraccount/envs/demo-app-dev/deployments',
      'description': None,
      'html_url': 'https://www.distelli.com/youraccount/envs/demo-app-dev',
      'last_deployment_url': 'https://api.distelli.com/youraccount/deployments/121509',
      'name': 'demo-app-dev',
      'owner': 'youraccount',
      'server_count': 1,
      'servers_url': 'https://api.distelli.com/youraccount/envs/demo-app-dev/servers',
      'settings_url': 'https://api.distelli.com/youraccount/envs/demo-app-dev/settings',
      'tags': [],
      'vars': [{'name': 'ENV_FOLDER', 'value': '"/var/conf/env/dev"'}]},
     {'active_release_url': 'https://api.distelli.com/youraccount/apps/demo-app/releases/v1',
      'active_release_version': 'v1',
      'api_url': 'https://api.distelli.com/youraccount/envs/demo-app-preview',
      'app_name': 'demo-app',
      'app_url': 'https://api.distelli.com/youraccount/apps/demo-app',
      'deployments_url': 'https://api.distelli.com/youraccount/envs/demo-app-preview/deployments',
      'description': None,
      'html_url': 'https://www.distelli.com/youraccount/envs/demo-app-preview',
      'last_deployment_url': 'https://api.distelli.com/youraccount/deployments/121515',
      'name': 'demo-app-preview',
      'owner': 'youraccount',
      'server_count': 1,
      'servers_url': 'https://api.distelli.com/youraccount/envs/demo-app-preview/servers',
      'settings_url': 'https://api.distelli.com/youraccount/envs/demo-app-preview/settings',

### Get details for a specific environment

	client.env('demo-app-preview')

Results are the same as `envs()` above, but only show the app specified.

### Create an environment

    client.create_env('demo-app-live', 'Description of the environment')

Results are the same as `env()` above, but only show the environment that was added.

### Delete an environment

    client.delete_env('demo-app-live')

### Add servers to an environment

    client.add_env_servers('demo-app-live', ['server-id-1', 'server-id-2'])

### Remove servers from an environment

    client.remove_env_servers('demo-app-live', ['server-id-1', 'server-id-2'])

## Server operations

### View your existing servers:

Just run:

	envs = client.servers()

Results appear as a Python dict:

    [{'agent_version': '3.63',
      'api_url': 'https://api.distelli.com/youraccount/servers/766b88c8-e925-11e4-ae8b-080027cc07f7',
      'cloud_instance_id': None,
      'cloud_location': None,
      'cloud_provider': None,
      'dns_name': 'demo-app-preview.youraccount.com',
      'html_url': 'https://www.distelli.com/youraccount/servers/766b88c8-e925-11e4-ae8b-080027cc07f7',
      'ip_addr': '192.168.1.112',
      'is_healthy': 'true',
      'mac_address': '08:00:27:cc:07:f7',
      'os_name': 'Ubuntu',
      'os_version': '14.04',
      'server_id': '766b88c8-e925-11e4-ae8b-080027cc07f7',
      'start_time': '2016-07-26T09:16:41.353Z',
      'tags': ['becon', 'beta', 'preview']},
     {'agent_version': '3.66',
      'api_url': 'https://api.distelli.com/youraccount/servers/a4d253a3-1668-e64b-86be-122d4227c561',
      'cloud_instance_id': 'i-9b668b5317f00995d',
      'cloud_location': 'eu-west-1',
      'cloud_provider': 'Aws',
      'dns_name': 'demo-app-live.youraccount.com',
      'html_url': 'https://www.distelli.com/youraccount/servers/a4d253a3-1668-e64b-86be-122d4227c561',
      'ip_addr': '10.226.127.83',
      'is_healthy': 'false',
      'mac_address': '12:2d:42:27:c5:61',
      'os_name': 'Ubuntu',
      'os_version': '14.04',
      'server_id': 'a4d253a3-1668-e64b-86be-122d4227c561',
      'start_time': '2016-12-20T19:39:32.835Z',
      'tags': None}]

### Get details for a specific server

	client.server('a4d253a3-1668-e64b-86be-122d4227c561')

Results are the same as `servers()` above, but only show the server specified.

### Remove a server from your account

	client.delete_server('a4d253a3-1668-e64b-86be-122d4227c561')

## Testing

To run the tests you will need a Distelli account and you will need to know your Distelli username and API token. As described in https://www.distelli.com/docs/api/getting-started-with-distelli-api

The tests will create and remove artifacts in your account.

Create a virtualenv (e.g. `mkvirtualenv --python=$(which python3) distelli-python`)

Install the requirements. `pip install -r requirements.txt`

Run the tests with your username and API token set using the environment variables `DISTELLI_TEST_USERNAME` and `DISTELLI_TEST_API_TOKEN`:

    DISTELLI_TEST_USERNAME=<username> DISTELLI_TEST_API_TOKEN=<api_token> make test
