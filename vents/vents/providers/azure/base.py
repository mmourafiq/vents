import logging
import os

from typing import List, Optional, Union

from vents.settings import VENTS_CONFIG

logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("azure.storage").setLevel(logging.WARNING)
logging.getLogger("azure.storage.blob").setLevel(logging.WARNING)


def get_account_name(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
) -> Optional[str]:
    # Check kwargs
    value = kwargs.get("account_name") or kwargs.get("AZURE_ACCOUNT_NAME")
    if value:
        return value
    # Check env/path keys
    keys = keys or ["AZURE_ACCOUNT_NAME"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_account_key(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
) -> Optional[str]:
    value = kwargs.get("account_key") or kwargs.get("AZURE_ACCOUNT_KEY")
    if value:
        return value
    keys = keys or ["AZURE_ACCOUNT_KEY"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_connection_string(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
) -> Optional[str]:
    value = kwargs.get("connection_string") or kwargs.get("AZURE_CONNECTION_STRING")
    if value:
        return value
    keys = keys or ["AZURE_CONNECTION_STRING"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_sas_token(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
) -> Optional[str]:
    value = (
        kwargs.get("sas_token")
        or kwargs.get("AZURE_SAS_TOKEN")
        or kwargs.get("AZURE_STORAGE_SAS_TOKEN")
    )
    if value:
        return value
    keys = keys or ["AZURE_SAS_TOKEN", "AZURE_STORAGE_SAS_TOKEN"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_tenant_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
) -> Optional[str]:
    value = kwargs.get("tenant_id") or kwargs.get("AZURE_TENANT_ID")
    if value:
        return value
    keys = keys or ["AZURE_TENANT_ID"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_client_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
) -> Optional[str]:
    value = kwargs.get("client_id") or kwargs.get("AZURE_CLIENT_ID")
    if value:
        return value
    keys = keys or ["AZURE_CLIENT_ID"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_client_secret(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs
) -> Optional[str]:
    value = kwargs.get("client_secret") or kwargs.get("AZURE_CLIENT_SECRET")
    if value:
        return value
    keys = keys or ["AZURE_CLIENT_SECRET"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def set_env_vars(
    account_name: Optional[str] = None,
    account_key: Optional[str] = None,
    connection_string: Optional[str] = None,
):
    if account_name:
        os.environ["AZURE_ACCOUNT_NAME"] = account_name
    if account_key:
        os.environ["AZURE_ACCOUNT_KEY"] = account_key
    if connection_string:
        os.environ["AZURE_CONNECTION_STRING"] = connection_string
