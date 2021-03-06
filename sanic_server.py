import asyncio
from aiohttp import web
from aiohttp import ClientSession

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from novaclient import client as nova_client
from glanceclient import client as glance_client
from neutronclient.v2_0 import client as neutron_client

import uvloop
import json

from sanic import Sanic
from sanic.response import HTTPResponse

app = Sanic()

AUTH_URL = 'http://10.220.104.33:5000/v3'
USERNAME = "admin"
PASSWORD = "admin"
PROJECT_NAME = "admin"
USER_DOMAIN_ID = "default"
PROJECT_DOMAIN_ID = "default"

NOVA_ENDPOINT = 'http://10.220.104.33:8774/v2.1'
GLANCE_ENDPOINT = 'http://10.220.104.33:9292/v2'
NEUTRON_ENDPOINT = 'http://10.220.104.33:9696/v2.0'

@app.route("/")
async def get_data(request):
    auth_token = get_auth_token()
    res_list = await asyncio.gather(
        list_flavors(auth_token),
        list_servers(auth_token),
        list_images(auth_token),
        list_networks(auth_token),
        list_ports(auth_token),
        list_fips(auth_token),
    )
    response = HTTPResponse(body="\n".join(
        [str(x) for x in res_list]).encode())
    return response

async def list_flavors(auth_token):

    url = '%s/flavors/detail' % NOVA_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['flavors']]

async def list_servers(auth_token):

    url = '%s/servers/detail' % NOVA_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['servers']]

async def list_images(auth_token):

    url = '%s/images' % GLANCE_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['images']]

async def list_networks(auth_token):

    url = '%s/networks.json' % NEUTRON_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['networks']]

async def list_ports(auth_token):

    url = '%s/ports.json' % NEUTRON_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['ports']]

async def list_fips(auth_token):

    url = '%s/floatingips.json' % NEUTRON_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['floating_ip_address'] for s in response['floatingips']]

def get_auth_token():
    auth = v3.Password(auth_url=AUTH_URL, username=USERNAME,
                    password=PASSWORD, project_name=PROJECT_NAME,
                    user_domain_id=USER_DOMAIN_ID, project_domain_id=PROJECT_DOMAIN_ID)
    sess = session.Session(auth=auth)
    return sess.get_token()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
