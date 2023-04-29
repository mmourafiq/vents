from typing import Optional

from adlfs import AzureBlobFileSystem as BaseAzureBlobFileSystem

from vents.providers.azure.service import AzureService


class AzureBlobFileSystem(BaseAzureBlobFileSystem):
    async def _put_file(self, lpath, rpath, delimiter="/", overwrite=True, **kwargws):
        return await super()._put_file(
            lpath, rpath, delimiter=delimiter, overwrite=overwrite, **kwargws
        )

    async def _ls(
        self,
        path: str,
        force: bool = False,
        delimiter: str = "/",
        return_glob: bool = False,
        **kwargs,
    ):
        invalidate_cache = kwargs.pop("invalidate_cache", force)
        return await super()._ls(
            path,
            invalidate_cache=invalidate_cache,
            delimiter=delimiter,
            return_glob=return_glob,
            **kwargs,
        )


class BlobStorageService(AzureService):
    def _set_session(
        self,
        asynchronous: Optional[bool] = False,
        use_listings_cache: Optional[bool] = False,
        **kwargs,
    ):
        self._session = AzureBlobFileSystem(
            account_name=self.account_name,
            account_key=self.account_key,
            connection_string=self.connection_string,
            sas_token=self.sas_token,
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret,
            asynchronous=asynchronous,
            use_listings_cache=use_listings_cache,
            **kwargs,
        )

    def get_fs(
        self,
        asynchronous: Optional[bool] = False,
        use_listings_cache: Optional[bool] = False,
        **kwargs,
    ):
        self._set_session(
            asynchronous=asynchronous, use_listings_cache=use_listings_cache, **kwargs
        )
        return self.session
