import api
from time import time
from application import Application, API_key_prompt

def check_client_id_and_secret(client_id: str | None, client_secret: str | None) -> None:
    # If no client ID or secret, request from user
    if not client_id or not client_secret:
        API_key_prompt().mainloop


def check_token_validity(client_id: str, client_secret: str, expiration: float) -> None:
    # If expired access token, request new token
    if expiration <= time():
        access_token, expiration = api.request_access_token(client_id, client_secret)
        api.write_to_env(client_id, client_secret, access_token, expiration)
    

def main():
    # Check for access token in .env
    client_id = api.get_client_id()
    client_secret = api.get_client_secret()
    expiration = api.get_access_token_expiration()

    # Check validity of client ID/secret and access token
    check_client_id_and_secret(client_id, client_secret)
    check_token_validity(client_id, client_secret, expiration)

    # Load application
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()