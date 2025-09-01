import api
from application import Application, API_key_prompt


def main():
    # Check for API key in .env
    client_id = api.get_client_id()
    client_secret = api.get_client_secret()

    if not client_id or not client_secret:
        prompt = API_key_prompt()
        prompt.mainloop()

    client_id = api.get_client_id()
    client_secret = api.get_client_secret()

    if client_id and client_secret:
        # Request API access token
        # print(f'Requesting access token using Client ID {client_id} and Client Secret {client_secret}')
        # access_token = api.request_access_token(client_id, client_secret)
        # print(f'Access token: {access_token}')

        # Load application
        app = Application()
        app.mainloop()


if __name__ == '__main__':
    main()