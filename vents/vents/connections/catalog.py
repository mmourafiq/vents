from typing import Dict, List, Optional

from clipped.config.schema import BaseSchemaModel
from pydantic import PrivateAttr

from vents.connections.connection import Connection
from vents.connections.k8s_resource import K8sResource


class ConnectionCatalog(BaseSchemaModel):
    connections: Optional[List[Connection]]
    _all_connections: List[Connection] = PrivateAttr()
    _secrets: Optional[List[K8sResource]] = PrivateAttr()
    _config_maps: Optional[List[K8sResource]] = PrivateAttr()
    _connections_by_names: Dict[str, Connection] = PrivateAttr()

    def set_all_connections(self) -> None:
        self._all_connections = self.connections[:] if self.connections else []
        self._connections_by_names = {}

    @property
    def all_connections(self) -> List[Connection]:
        return self._all_connections

    @property
    def secrets(self) -> List[K8sResource]:
        if self._secrets or not self._all_connections:
            return self._secrets
        secret_names = set()
        secrets = []
        for c in self._all_connections:
            if c.secret and c.secret.name not in secret_names:
                secret_names.add(c.secret.name)
                secrets.append(c.secret)
        self._secrets = secrets
        return self._secrets

    @property
    def config_maps(self) -> List[K8sResource]:
        if self._config_maps or not self._all_connections:
            return self._config_maps
        config_map_names = set()
        config_maps = []
        for c in self._all_connections:
            if c.config_map and c.config_map.name not in config_map_names:
                config_map_names.add(c.config_map.name)
                config_maps.append(c.config_map)
        self._config_maps = config_maps
        return self._config_maps

    @property
    def connections_by_names(self) -> Dict[str, Connection]:
        if self._connections_by_names or not self._all_connections:
            return self._connections_by_names

        self._connections_by_names = {c.name: c for c in self._all_connections}
        return self._connections_by_names
