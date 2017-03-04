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


AUTH_URL = 'http://10.220.101.33:5000/v3'
USERNAME = "admin"
PASSWORD = "admin"
PROJECT_NAME = "admin"
USER_DOMAIN_ID = "default"
PROJECT_DOMAIN_ID = "default"


@app.route("/")
async def hello(request):
    auth_token = get_auth_token()
    await asyncio.gather(
        list_flavors(auth_token),
        list_servers(auth_token),
        list_images(auth_token),
        list_networks(auth_token),
        list_ports(auth_token),
        list_fips(auth_token),
    )
    #response = web.Response(body="Servers: {}\nImages: {}\nFlavors: {}\n".format(servers, images, flavors).encode())
    response = HTTPResponse(body="Getrekt".encode())
    return response

async def list_flavors(auth_token):

    url = 'http://10.220.101.33:8774/v2.1/flavors/detail'
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['flavors']]

async def list_servers(auth_token):

    url = 'http://10.220.101.33:8774/v2.1/servers/detail'
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['servers']]

async def list_images(auth_token):

    url = 'http://10.220.101.33:9292/v2/images'
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()
            return [s['name'] for s in response['images']]

async def list_networks(auth_token):

    url = 'http://10.220.101.33:9696/v2.0/networks.json'
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.read()

async def list_ports(auth_token):

    url = 'http://10.220.101.33:9696/v2.0/ports.json'
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.json()

async def list_fips(auth_token):

    url = 'http://10.220.101.33:9696/v2.0/floatingips.json'
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response = await response.read()

def get_auth_token():
    auth = v3.Password(auth_url=AUTH_URL, username=USERNAME,
                    password=PASSWORD, project_name=PROJECT_NAME,
                    user_domain_id=USER_DOMAIN_ID, project_domain_id=PROJECT_DOMAIN_ID)
    sess = session.Session(auth=auth)
    return sess.get_token()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
