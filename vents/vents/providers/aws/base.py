from typing import List, Optional, Union

from vents.settings import VENTS_CONFIG


def get_aws_access_key_id(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = (
        kwargs.get("access_key_id")
        or kwargs.get("aws_access_key_id")
        or kwargs.get("AWS_ACCESS_KEY_ID")
    )
    if value:
        return value
    keys = keys or ["AWS_ACCESS_KEY_ID"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_aws_secret_access_key(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = (
        kwargs.get("secret_access_key")
        or kwargs.get("aws_secret_access_key")
        or kwargs.get("AWS_SECRET_ACCESS_KEY")
    )
    if value:
        return value
    keys = keys or ["AWS_SECRET_ACCESS_KEY"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_aws_security_token(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = (
        kwargs.get("session_token")
        or kwargs.get("aws_session_token")
        or kwargs.get("security_token")
        or kwargs.get("aws_security_token")
        or kwargs.get("AWS_SECURITY_TOKEN")
    )
    if value:
        return value
    keys = keys or ["AWS_SECURITY_TOKEN"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_region(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = (
        kwargs.get("region")
        or kwargs.get("region_name")
        or kwargs.get("aws_region")
        or kwargs.get("AWS_REGION")
    )
    if value:
        return value
    keys = keys or ["AWS_REGION"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_endpoint_url(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> Optional[str]:
    value = (
        kwargs.get("endpoint_url")
        or kwargs.get("aws_endpoint_url")
        or kwargs.get("AWS_ENDPOINT_URL")
    )
    if value:
        return value
    keys = keys or ["AWS_ENDPOINT_URL"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_aws_use_ssl(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> bool:
    value = (
        kwargs.get("use_ssl") or kwargs.get("aws_use_ssl") or kwargs.get("AWS_USE_SSL")
    )
    if value is not None:
        return value
    keys = keys or ["AWS_USE_SSL"]
    value = VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore
    if value is not None:
        return value
    return True


def get_aws_verify_ssl(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> bool:
    value = kwargs.get(
        "verify_ssl",
        kwargs.get("aws_verify_ssl", kwargs.get("AWS_VERIFY_SSL", None)),
    )
    if value is not None:
        return value
    keys = keys or ["AWS_VERIFY_SSL"]
    value = VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore
    if value is not None:
        return value
    return True


def get_aws_legacy_api(
    keys: Optional[Union[str, List[str]]] = None,
    context_path: Optional[str] = None,
    **kwargs,
) -> bool:
    value = (
        kwargs.get("legacy_api")
        or kwargs.get("aws_legacy_api")
        or kwargs.get("AWS_LEGACY_API")
    )
    if value:
        return value
    keys = keys or ["AWS_LEGACY_API"]
    return VENTS_CONFIG.read_keys(context_path=context_path, keys=keys)  # type: ignore


def get_legacy_api(legacy_api=False, **kwargs):
    legacy_api = legacy_api or get_aws_legacy_api(**kwargs)
    return legacy_api


def get_aws_session(
    context_path=None,
    **kwargs,
):
    import boto3

    aws_access_key_id = get_aws_access_key_id(context_path=context_path, **kwargs)
    aws_secret_access_key = get_aws_secret_access_key(
        context_path=context_path, **kwargs
    )
    aws_session_token = get_aws_security_token(context_path=context_path, **kwargs)
    region_name = get_region(context_path=context_path, **kwargs)
    return boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
    )


def get_aws_client(
    client_type,
    context_path=None,
    **kwargs,
):
    session = get_aws_session(
        context_path=context_path,
        **kwargs,
    )
    endpoint_url = get_endpoint_url(context_path=context_path, **kwargs)
    aws_use_ssl = get_aws_use_ssl(context_path=context_path, **kwargs)
    aws_verify_ssl = get_aws_verify_ssl(context_path=context_path, **kwargs)
    return session.client(
        client_type,
        endpoint_url=endpoint_url,
        use_ssl=aws_use_ssl,
        verify=aws_verify_ssl,
    )


def get_aws_resource(
    resource_type,
    context_path=None,
    **kwargs,
):
    session = get_aws_session(
        context_path=context_path,
        **kwargs,
    )
    endpoint_url = get_endpoint_url(context_path=context_path, **kwargs)
    aws_use_ssl = get_aws_use_ssl(context_path=context_path, **kwargs)
    aws_verify_ssl = get_aws_verify_ssl(context_path=context_path, **kwargs)
    return session.resource(
        resource_type,
        endpoint_url=endpoint_url,
        use_ssl=aws_use_ssl,
        verify=aws_verify_ssl,
    )
