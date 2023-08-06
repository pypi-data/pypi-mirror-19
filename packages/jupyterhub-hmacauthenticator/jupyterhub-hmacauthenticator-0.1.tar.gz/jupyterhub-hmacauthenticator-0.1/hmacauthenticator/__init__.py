import hmac
import hashlib

from jupyterhub.auth import Authenticator
from tornado import gen
from traitlets import Bytes


class HMACAuthenticator(Authenticator):
    """
    JupyterHub authenticator where the password is HMAC of username + secret key.

    Useful when you want to procedurally generate many users
    to test your JupyterHub install. This is more secure
    than DummyAuthenticator and much simpler than most other
    password based authenticators.
    """

    secret_key = Bytes(
        config=True,
        help="""
        Hex encoded secret key to use for deriving the HMAC.

        Recommend generating with `openssl rand -hex 64`,
        which provides a 512-bit secret key.
        """
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        sha512_hmac = hmac.new(
            self.secret_key,
            data['username'].encode('utf-8'),
            hashlib.sha512
        )
        if hmac.compare_digest(sha512_hmac.hexdigest(), data['password']):
            return data['username']
        return None
