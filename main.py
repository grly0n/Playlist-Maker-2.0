import api
from time import time
from application import Application, API_key_prompt


def main():
    # Check for access token in .env
    access_token = api.get_access_token()
    expiration = float(api.get_access_token_expiration())

    # If no or expired access token, request new token
    if not access_token or expiration <= time():
        prompt = API_key_prompt()
        prompt.mainloop()

    # If access token successfully acquired, launch application
    if api.get_access_token():
        # Load application
        app = Application()
        app.mainloop()


if __name__ == '__main__':
    main()