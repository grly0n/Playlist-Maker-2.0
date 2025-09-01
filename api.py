import os
import requests
import base64
from dotenv import load_dotenv

def get_client_id():
    load_dotenv()
    api_key = os.getenv('SPOTIFY_CLIENT_ID')
    if api_key: return api_key
    client_id = input('Please enter your Spotify API client ID: ')
    with open('.env') as file:
        file.write(f'SPOTIFY_CLIENT_ID={client_id}')


def get_client_secret():
    load_dotenv()
    api_key = os.getenv('SPOTIFY_CLIENT_SECRET')
    if api_key: return api_key
    client_secret = input('Please enter your Spotify API client secret: ')
    with open('.env') as file:
        file.write(f'SPOTIFY_CLIENT_SECRET={client_secret}')


def request_access_token(client_id: str, client_secret: str):
    encoded_string = str(base64.b64encode(bytes(f'{client_id}:{client_secret}', 'utf-8')))
    response = requests.post(url='https://accounts.spotify.com/api/token', headers={'Authorization': 'Basic ' + encoded_string, 'Content-Type': 'applicaiton/x-www-form-urlencoded'}, 
                     data={'grant_type': 'client_credentials'})
    print(response)