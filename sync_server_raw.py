from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver


AUTH_URL = "http://10.220.104.33:5000/v3"
USERNAME = "admin"
PASSWORD = "admin"
PROJECT_NAME = "admin"
USER_DOMAIN_ID = "default"
PROJECT_DOMAIN_ID = "default"

GLANCE_ENDPOINT = 'http://10.220.104.33:9292/v2'
NEUTRON_ENDPOINT = 'http://10.220.104.33:9696/v2.0'
NOVA_ENDPOINT = 'http://10.220.104.33:8774/v2.1'


def get_auth_token():
    auth = v3.Password(auth_url=AUTH_URL, username=USERNAME,
                    password=PASSWORD, project_name=PROJECT_NAME,
                    user_domain_id=USER_DOMAIN_ID, project_domain_id=PROJECT_DOMAIN_ID)
    sess = session.Session(auth=auth)
    return sess.get_token()

def list_flavors(auth_token):
    url = '%s/flavors/detail' % NOVA_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers).json()
    return [s['name'] for s in response['flavors']]

def list_servers(auth_token):
    url = '%s/servers/detail' % NOVA_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers).json()
    return [s['name'] for s in response['servers']]

def list_images(auth_token):
    url = '%s/images' % GLANCE_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers).json()
    return [s['name'] for s in response['images']]

def list_ports(auth_token):
    url = '%s/ports.json' % NEUTRON_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers).json()
    return [s['name'] for s in response['ports']]

def list_fips(auth_token):
    url = '%s/floatingips.json' % NEUTRON_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers).json()
    return [s['floating_ip_address'] for s in response['floatingips']]

def list_networks(auth_token):
    url = '%s/networks.json' % NEUTRON_ENDPOINT
    headers = {'content-type': 'application/json', 'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers).json()
    return [s['name'] for s in response['networks']]

def get_data():
    auth_token = get_auth_token()
    flavors = list_flavors(auth_token)
    images = list_images(auth_token)
    servers = list_servers(auth_token)
    networks = list_networks(auth_token)
    ports = list_ports(auth_token)
    fips = list_fips(auth_token)

    return "\n".join([str(x) for x in [flavors, servers, images, networks, ports, fips]])

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        response = get_data()
        self.wfile.write(response.encode())

def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
