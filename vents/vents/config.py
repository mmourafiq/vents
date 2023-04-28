import logging
import os

from typing import Any, List, Optional, Set, Type, Union

from clipped.config.parser import ConfigParser
from clipped.config.schema import BaseSchemaModel
from clipped.types import Uri
from clipped.utils.paths import check_dirname_exists
from pydantic import ValidationError

from vents.connections.connection import Connection
from vents.exceptions import VentError

_logger = logging.getLogger("vents.config.reader")


class AppConfig(BaseSchemaModel):
    project_name: Optional[str] = "Vents"
    project_url: Optional[Uri] = ""
    project_icon: Optional[Uri] = ""
    env_prefix: Optional[str] = "VENTS"
    context_path: Optional[str] = ""
    logger: Any = _logger
    exception: Type[Exception] = VentError
    config_parser: Type[ConfigParser] = ConfigParser

    def get_from_env(self, keys: Union[Set[str], List[str], str]) -> Any:
        """
        Returns a variable from one of the list of keys based on the os.env.
        Args:
            keys: list(str). list of keys to check in the environment

        Returns:
            str | None
        """
        keys = keys or []
        if not isinstance(keys, (list, tuple, set)):
            keys = [keys]
        for key in keys:
            value = os.environ.get(key)
            if value:
                if value.lower() == "true":
                    return True
                if value.lower() == "false":
                    return False
                return value
            # Prepend prefix if set
            if self.env_prefix:
                key = "{}_{}".format(self.env_prefix, key)
                value = os.environ.get(key)
                if value:
                    return value

        return None

    def get_from_path(
        self, context_paths: List[str], keys: Union[Set[str], List[str], str]
    ) -> Optional[Any]:
        """
        Returns a variable from one of the list of keys based on a base path.
        Args:
            context_paths: List[str], base path where to look for keys.
            keys: list(str). list of keys to check in the environment

        Returns:
            str | None
        """
        context_paths = context_paths or []
        context_paths = [
            c for c in context_paths if check_dirname_exists(c, is_dir=True)
        ]
        if not context_paths:
            return None

        keys = keys or []
        if not isinstance(keys, (list, tuple)):
            keys = [keys]  # type: ignore
        for key in keys:
            for context_path in context_paths:
                key_path = os.path.join(context_path, key)
                if not os.path.exists(key_path):
                    continue
                with open(key_path) as f:
                    value = f.read()
                    if value:
                        if value.lower() == "true":
                            return True
                        if value.lower() == "false":
                            return False
                        return value

        return None

    def get_connection_context_path_env_name(self, name: str) -> str:
        env_name = "CONNECTION_CONTEXT_PATH_".format(name.upper())
        if self.env_prefix:
            env_name = "{}_{}".format(self.env_prefix, env_name)
        return env_name

    def get_connection_schema_env_name(self, name: str) -> str:
        env_name = "CONNECTION_SCHEMA_".format(name.upper())
        if self.env_prefix:
            env_name = "{}_{}".format(self.env_prefix, env_name)
        return env_name

    def get_connection_context_path(self, name: Optional[str]) -> Optional[str]:
        """Checks if a connection has a mount path exported"""
        if not name:
            return None

        context_path = os.environ.get(self.get_connection_context_path_env_name(name))
        if not context_path:
            return None

        if not os.path.exists(context_path):
            self.logger.warning(
                "A connection path was found for {}, "
                "but a path the {} does not exist.".format(name, context_path)
            )
            return None
        return context_path

    def get_connection_type(self, name: Optional[str]) -> Optional[Connection]:
        """Checks if a connection has a mount path exported"""
        if not name:
            return None

        spec = os.environ.get(self.get_connection_schema_env_name(name))
        if not spec:
            return None

        try:
            return Connection.read(spec, config_type=".json")
        except ValidationError as e:
            self.logger.warning(
                "A connection spec was found for {}, "
                "but the reading the spec raised an error {}.".format(name, repr(e))
            )
            return None

    def read_keys(self, context_paths: List[str], keys: List[str]) -> Optional[Any]:
        """Returns a variable by checking first a context path and then in the environment."""
        keys = (
            {k.lower() for k in keys}
            | {k.upper() for k in keys}
            | {"".join(k.lower().split("_")) for k in keys}
        )
        if context_paths:
            value = self.get_from_path(context_paths=context_paths, keys=keys)
            if value is not None:
                return value
        return self.get_from_env(keys)
