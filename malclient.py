
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new
import requests
import secrets
import json
import os
from malanime import *
class HTTPServerHandler(BaseHTTPRequestHandler):

    def __init__(self, request, address, server):
        super().__init__(request, address, server)

    def do_GET(self):
        #BASE_URI = 'https://myanimelist.net/v%i/oauth2/authorize' % self.api_version
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if('code' in self.path):
            self.server.auth_code = self.path.split('=')[1]
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                         + '</h1></html>', 'utf-8'))
        else:
            self.server.auth_code = None
            self.wfile.write(bytes('<html><h1>Error.'
                         + '</h1></html>', 'utf-8'))

class MALCLient():

    def __init__(self, client_id, client_secret=None):
        self.client_id = client_id
        self.client_secret = client_secret
    def get_new_code_verifier(self) -> str:
        token = secrets.token_urlsafe(100)
        return token[:128]
    
    def load_previous_token(self, filename='mal_token.json'):
        if(os.path.isfile(filename)):
            with open(filename, 'r') as file:
                self.token = json.load(file)
                print('Token loaded successfully!')
                return True
        else:
            return False
    
    def login(self, api_version=1):
        self.code_challenge = self.get_new_code_verifier()
        auth_url = 'https://myanimelist.net/v%i/oauth2/authorize?response_type=code&client_id=%s&code_challenge=%s' % (api_version, self.client_id, self.code_challenge)
        open_new(auth_url)
        httpServer = HTTPServer(
                ('localhost', 5000),
                lambda request, address, server: HTTPServerHandler(
                    request, address, server))
        httpServer.handle_request()
        self.auth_code = httpServer.auth_code
        user_url = 'https://myanimelist.net/v1/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.auth_code,
            'code_verifier': self.code_challenge,
            'grant_type': 'authorization_code'
        }
        response = requests.post(user_url, data)
        response.raise_for_status()
        self.token = response.json()
        response.close()
        print('Token generated successfully!')

        with open('mal_token.json', 'w') as file:
            json.dump(self.token, file, indent = 4)
            print('Token saved in "mal_token.json"')


with requests.get('https://mangaupdates.com/ajax/find_categories.php') as response:
    print(response.text)
client = MALCLient('3ce013c603730d0ee80d7f6c626a30bf')
if not client.load_previous_token():
    client.login()
anime = MALAnime(client.token)
anime.get_anime_list('Dragon Ball',10)



