from rest_framework.authentication import TokenAuthentication


class APIUser:
    def __init__(self, access_token):
        self.access_token = access_token

    @property
    def is_authenticated(self):
        return True


class APIAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, access_token):
        return (APIUser(access_token), access_token)
