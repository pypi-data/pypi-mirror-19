# The idea of these exceptions copied from
# https://stripe.com/docs/api?lang=python#errors


class StampsError(Exception):

    def __init__(self, http_status, error_messages, response=None):
        self.http_status = http_status
        self.error_messages = error_messages
        self.response = response


class ServerError(StampsError):
    pass


class ConnectionError(StampsError):
    pass


class AuthenticationError(StampsError):
    pass


class InvalidRequest(StampsError):
    pass
