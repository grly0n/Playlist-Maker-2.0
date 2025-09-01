import os
import requests
import base64
from time import time
from dotenv import load_dotenv

def get_client_id():
    load_dotenv()
    return os.getenv('SPOTIFY_CLIENT_ID')


def get_client_secret():
    load_dotenv()
    return os.getenv('SPOTIFY_CLIENT_SECRET')


def get_access_token():
    load_dotenv()
    return os.getenv('SPOTIFY_ACCESS_TOKEN')


def get_access_token_expiration():
    load_dotenv()
    return os.getenv('ACCESS_TOKEN_EXPIRATION')


def request_access_token(client_id: str, client_secret: str):
    auth_header = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token'], token_info['expires_in'] + time()
    else:
        return '', 0
    

def write_to_env(client_id: str, client_secret: str, access_token: str, expiration: float):
    with open('.env', 'w') as file:
        file.write(f'SPOTIFY_CLIENT_ID={client_id}\n')
        file.write(f'SPOTIFY_CLIENT_SECRET={client_secret}\n')
        file.write(f'SPOTIFY_ACCESS_TOKEN={access_token}\n')
        file.write(f'ACCESS_TOKEN_EXPIRATION={expiration}')