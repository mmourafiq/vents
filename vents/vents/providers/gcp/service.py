import json
import os

from typing import TYPE_CHECKING, Any, List, Optional

from google.oauth2.service_account import Credentials

from vents.providers.base import BaseService
from vents.providers.gcp.base import (
    get_default_key_path,
    get_gc_credentials,
    get_key_path,
    get_keyfile_dict,
    get_project_id,
    get_scopes,
)

if TYPE_CHECKING:
    from google.cloud.storage.client import Client

    from vents.connections.connection import Connection


class GCPService(BaseService):
    project_id: Optional[str]
    key_path: Optional[str]
    keyfile_dict: Optional[str]
    scopes: Optional[List[str]]
    credentials: Optional[Credentials]
    client_info = Optional[Any]
    client_options = Optional[Any]
    encoding: Optional[str] = "utf-8"

    @classmethod
    def load_from_connection(
        cls, connection: Optional["Connection"]
    ) -> Optional["GCPService"]:
        # Check if there are mounting based on secrets/configmaps
        context_paths = []
        if connection:
            if connection.secret and connection.secret.mount_path:
                context_paths.append(connection.secret.mount_path)
            if connection.config_map and connection.config_map.mount_path:
                context_paths.append(connection.config_map.mount_path)
        project_id = get_project_id(context_paths=context_paths)
        key_path = get_key_path(context_paths=context_paths)
        keyfile_dict = get_keyfile_dict(context_paths=context_paths)
        scopes = get_scopes(context_paths=context_paths)
        credentials = get_gc_credentials(
            key_path=key_path,
            keyfile_dict=keyfile_dict,
            scopes=scopes,
        )
        return cls(
            project_id=project_id,
            key_path=key_path,
            keyfile_dict=keyfile_dict,
            scopes=scopes,
            credentials=credentials,
        )

    def _set_session(self):
        self._session = Client(
            project=self.project_id,
            credentials=self.credentials,
            client_info=self.client_info,
            client_options=self.client_options,
        )

    def set_env_vars(self):
        if self.key_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.key_path
        elif self.keyfile_dict:
            key_path = get_default_key_path()
            with open(key_path, "w") as outfile:
                json.dump(self.keyfile_dict, outfile)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
