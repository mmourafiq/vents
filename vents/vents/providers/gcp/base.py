import os

from collections.abc import Mapping
from typing import Any, Dict, List, Optional, Union

import google.auth
import google.oauth2.service_account

from clipped.utils.json import orjson_loads
from google.oauth2.service_account import Credentials

from vents.settings import VENTS_CONFIG

DEFAULT_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]


def get_default_key_path():
    return "{}/.gc/gc-secret.json".format(VENTS_CONFIG.context_path or "/tmp")


def get_project_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = kwargs.get("project_id")
    if value:
        return value
    keys = keys or [
        "GC_PROJECT",
        "GOOGLE_PROJECT",
        "GC_PROJECT_ID",
        "GOOGLE_PROJECT_ID",
    ]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_key_path(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = kwargs.get("key_path")
    if value:
        return value
    keys = keys or ["GC_KEY_PATH", "GOOGLE_KEY_PATH", "GOOGLE_APPLICATION_CREDENTIALS"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_keyfile_dict(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[Dict]:
    value = kwargs.get("keyfile_dict")
    if value:
        return value
    keys = keys or ["GC_KEYFILE_DICT", "GOOGLE_KEYFILE_DICT"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_scopes(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = kwargs.get("scopes")
    if value:
        return value
    keys = keys or ["GC_SCOPES", "GOOGLE_SCOPES"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_gc_credentials(
    context_path: Optional[str] = None,
    **kwargs,
) -> Credentials:
    """
    Returns the Credentials object for Google API
    """
    key_path = get_key_path(context_path=context_path, **kwargs)
    keyfile_dict = get_keyfile_dict(context_path=context_path, **kwargs)
    _scopes = get_scopes(context_path=context_path, **kwargs)

    if _scopes is not None:
        scopes = [s.strip() for s in _scopes.split(",")]
    else:
        scopes = DEFAULT_SCOPES

    if not key_path and not keyfile_dict:
        context_secret = get_default_key_path()
        # Look for default GC path
        if os.path.exists(context_secret):
            key_path = context_secret

    if not key_path and not keyfile_dict:
        VENTS_CONFIG.logger.info(
            "Getting connection using `google.auth.default()` "
            "since no key file is defined for hook."
        )
        credentials, _ = google.auth.default(scopes=scopes)
    elif key_path:
        # Get credentials from a JSON file.
        if key_path.endswith(".json"):
            VENTS_CONFIG.logger.info("Getting connection using a JSON key file.")
            credentials = Credentials.from_service_account_file(
                os.path.abspath(key_path), scopes=scopes
            )
        else:
            raise VENTS_CONFIG.exception("Unrecognised extension for key file.")
    else:
        # Get credentials from JSON data.
        try:
            if not isinstance(keyfile_dict, Mapping):
                keyfile_dict = orjson_loads(keyfile_dict)  # type: ignore

            # Convert escaped newlines to actual newlines if any.
            keyfile_dict["private_key"] = keyfile_dict["private_key"].replace(
                "\\n", "\n"
            )

            credentials = Credentials.from_service_account_info(
                keyfile_dict, scopes=scopes
            )
        except ValueError:  # json.decoder.JSONDecodeError does not exist on py2
            raise VENTS_CONFIG.exception("Invalid key JSON.")

    return credentials


def get_gc_access_token(
    credentials=None,
    context_path: Optional[str] = None,
    **kwargs,
) -> str:
    credentials = credentials or get_gc_credentials(context_path=context_path, **kwargs)
    return credentials.token


def get_gc_client(
    credentials=None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Any:
    from google.cloud.storage.client import Client

    credentials = credentials or get_gc_credentials(context_path=context_path, **kwargs)
    project_id = get_project_id(context_path=context_path, **kwargs)
    return Client(project=project_id, credentials=credentials)
