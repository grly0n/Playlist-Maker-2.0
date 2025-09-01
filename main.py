import api
from application import Application


def main():
    # Check for API key in .env
    client_id = api.get_client_id()
    client_secret = api.get_client_secret()
    
    # Request API access token
    api.request_access_token(client_id, client_secret)

    # Load application
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()