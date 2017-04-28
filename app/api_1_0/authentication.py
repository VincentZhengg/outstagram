from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def serializer():
    return Serializer("hard to guess", expires_in=3600)


def generate_auth_token():
    s = serializer()
    return s.dumps({'confirm': 23})


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(account, password):
    pass
