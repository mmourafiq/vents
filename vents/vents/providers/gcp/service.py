import json
import os

from typing import TYPE_CHECKING, List, Optional

from vents.providers.base import BaseService
from vents.providers.gcp.base import get_default_key_path, get_gc_client
from vents.settings import VENTS_CONFIG

if TYPE_CHECKING:
    from google.oauth2.service_account import Credentials

    from vents.connections.connection import Connection


class GCPService(BaseService):
    def __init__(self, connection=None, **kwargs):
        super().__init__(connection=connection, **kwargs)
        self._project_id = kwargs.get("project_id")
        self._credentials = kwargs.get("credentials")
        self._key_path = kwargs.get("key_path")
        self._keyfile_dict = kwargs.get("keyfile_dict")
        self._scopes = kwargs.get("scopes")
        self._encoding = kwargs.get("encoding", "utf-8")

    def set_connection(
        self,
        connection: Optional[str] = None,
        connection_type: Optional["Connection"] = None,
        project_id: Optional[str] = None,
        key_path: Optional[str] = None,
        keyfile_dict: Optional[str] = None,
        credentials: Optional["Credentials"] = None,
        scopes: Optional[List[str]] = None,
    ):
        """
        Sets a new gc client.

        Args:
            project_id: `str`. The project if.
            key_path: `str`. The path to the json key file.
            keyfile_dict: `str`. The dict containing the auth data.
            credentials: `Credentials instance`. The credentials to use.
            scopes: `list`. The scopes.

        Returns:
            Service client instance
        """
        if connection:
            self._connection = connection
            return
        connection_type = connection_type or self._connection_type
        connection_name = connection_type.name if connection_type else None
        context_path = VENTS_CONFIG.get_connection_context_path(name=connection_name)
        self._connection = get_gc_client(
            project_id=project_id or self._project_id,
            key_path=key_path or self._key_path,
            keyfile_dict=keyfile_dict or self._keyfile_dict,
            credentials=credentials or self._credentials,
            scopes=scopes or self._scopes,
            context_path=context_path,
        )

    def set_env_vars(self):
        if self._key_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self._key_path
        elif self._keyfile_dict:
            key_path = get_default_key_path()
            with open(key_path, "w") as outfile:
                json.dump(self._keyfile_dict, outfile)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
