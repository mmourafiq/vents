from typing import Dict, Optional

from s3fs import S3FileSystem as BaseS3FileSystem

from vents.providers.aws.service import AWSService


class S3FileSystem(BaseS3FileSystem):
    retries = 5

    async def _ls(self, path: str, detail: bool = False, force: bool = False):
        return await super()._ls(path, detail=detail, refresh=force)


class S3Service(AWSService):
    def _set_session(
        self,
        asynchronous: Optional[bool] = False,
        use_listings_cache: Optional[bool] = False,
        config_kwargs: Optional[Dict] = None,
        client_kwargs: Optional[Dict] = None,
        **kwargs
    ):
        self._session = S3FileSystem(
            key=self.access_key_id,
            secret=self.secret_access_key,
            token=self.session_token,
            use_ssl=self.use_ssl,
            config_kwargs=config_kwargs,
            client_kwargs=client_kwargs,
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            **kwargs,
        )

    def get_fs(
        self,
        asynchronous: Optional[bool] = False,
        use_listings_cache: Optional[bool] = False,
        config_kwargs: Optional[Dict] = None,
        client_kwargs: Optional[Dict] = None,
        **kwargs
    ):
        self._set_session(
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            config_kwargs=config_kwargs,
            client_kwargs=client_kwargs,
            **kwargs,
        )
        return self.session
