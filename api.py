import os
import requests
import base64
from time import time
from dotenv import load_dotenv

def get_client_id() -> str:
    load_dotenv()
    return os.getenv('SPOTIFY_CLIENT_ID')


def get_client_secret() -> str:
    load_dotenv()
    return os.getenv('SPOTIFY_CLIENT_SECRET')


def get_access_token() -> str:
    load_dotenv()
    return os.getenv('SPOTIFY_ACCESS_TOKEN')


def get_access_token_expiration() -> float:
    load_dotenv()
    return float(os.getenv('ACCESS_TOKEN_EXPIRATION'))


def request_access_token(client_id: str, client_secret: str) -> tuple[str, float]:
    auth_header = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token'], float(token_info['expires_in'] + time())
    else:
        return '', 0.0
    

def write_to_env(client_id: str, client_secret: str, access_token: str, expiration: float) -> None:
    with open('.env', 'w') as file:
        file.write(f'SPOTIFY_CLIENT_ID={client_id}\n')
        file.write(f'SPOTIFY_CLIENT_SECRET={client_secret}\n')
        file.write(f'SPOTIFY_ACCESS_TOKEN={access_token}\n')
        file.write(f'ACCESS_TOKEN_EXPIRATION={expiration}')


def parse_link(link: str) -> str:
    return link.split('/track/')[1].split('?')[0]


def request_song_info(link: str) -> requests.Response:
    id = parse_link(link)
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}
    return requests.get(f'https://api.spotify.com/v1/tracks/{id}', headers=headers)