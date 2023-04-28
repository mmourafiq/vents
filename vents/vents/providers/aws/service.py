import os

from typing import TYPE_CHECKING, Optional

from vents.providers.aws.base import (
    get_aws_access_key_id,
    get_aws_secret_access_key,
    get_aws_security_token,
    get_aws_use_ssl,
    get_aws_verify_ssl,
    get_endpoint_url,
    get_region,
)
from vents.providers.base import BaseService

if TYPE_CHECKING:
    from vents.connections.connection import Connection


class AWSService(BaseService):
    resource: Optional[str]
    region: Optional[str]
    endpoint_url: Optional[str]
    access_key_id: Optional[str]
    secret_access_key: Optional[str]
    session_token: Optional[str]
    verify_ssl: Optional[bool]
    use_ssl: Optional[bool]

    @classmethod
    def load_from_connection(
        cls, connection: Optional["Connection"]
    ) -> Optional["AWSService"]:
        # Check if there are mounting based on secrets/configmaps
        context_paths = []
        if connection:
            if connection.secret and connection.secret.mount_path:
                context_paths.append(connection.secret.mount_path)
            if connection.config_map and connection.config_map.mount_path:
                context_paths.append(connection.config_map.mount_path)
        region = get_region(context_paths=context_paths)
        endpoint_url = get_endpoint_url(context_paths=context_paths)
        access_key_id = get_aws_access_key_id(context_paths=context_paths)
        secret_access_key = get_aws_secret_access_key(context_paths=context_paths)
        verify_ssl = get_aws_verify_ssl(context_paths=context_paths)
        use_ssl = get_aws_use_ssl(context_paths=context_paths)
        session_token = get_aws_security_token(context_paths=context_paths)
        return cls(
            region=region,
            endpoint_url=endpoint_url,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
            verify_ssl=verify_ssl,
            use_ssl=use_ssl,
        )

    def _set_session(self):
        import boto3

        self._session = boto3.session.Session(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            aws_session_token=self.session_token,
            region_name=self.region,
        )

    def set_env_vars(self):
        if self.endpoint_url:
            os.environ["AWS_ENDPOINT_URL"] = self.endpoint_url
        if self.access_key_id:
            os.environ["AWS_ACCESS_KEY_ID"] = self.access_key_id
        if self.secret_access_key:
            os.environ["AWS_SECRET_ACCESS_KEY"] = self.secret_access_key
        if self.session_token:
            os.environ["AWS_SECURITY_TOKEN"] = self.session_token
        if self.region:
            os.environ["AWS_REGION"] = self.region
        if self.use_ssl is not None:
            os.environ["AWS_USE_SSL"] = str(self.use_ssl)
        if self.verify_ssl is not None:
            os.environ["AWS_VERIFY_SSL"] = str(self.verify_ssl)

    def get_client(self):
        return self.session.client(
            service_name=self.resource,
            region_name=self.region,
            endpoint_url=self.endpoint_url,
            use_ssl=self.use_ssl,
            verify=self.verify_ssl,
        )

    def get_resource(self):
        return self.session.resource(
            self.resource,
            endpoint_url=self.endpoint_url,
            use_ssl=self.use_ssl,
            verify=self.verify_ssl,
        )
