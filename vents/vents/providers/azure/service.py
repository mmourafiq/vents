import os

from vents.providers.base import BaseService


class AzureService(BaseService):
    def __init__(self, connection=None, **kwargs):
        super().__init__(connection=connection, **kwargs)
        self._account_name = kwargs.get("account_name") or kwargs.get(
            "AZURE_ACCOUNT_NAME"
        )
        self._account_key = kwargs.get("account_key") or kwargs.get("AZURE_ACCOUNT_KEY")
        self._connection_string = kwargs.get("connection_string") or kwargs.get(
            "AZURE_CONNECTION_STRING"
        )

    def set_connection(
        self,
        connection=None,
        connection_name=None,
        account_name=None,
        account_key=None,
        connection_string=None,
    ):
        raise NotImplementedError

    def set_env_vars(self):
        if self._account_name:
            os.environ["AZURE_ACCOUNT_NAME"] = self._account_name
        if self._account_key:
            os.environ["AZURE_ACCOUNT_KEY"] = self._account_key
        if self._connection_string:
            os.environ["AZURE_CONNECTION_STRING"] = self._connection_string
