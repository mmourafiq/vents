from typing import Dict, List, Optional, Union

from clipped.compact.pydantic import Field, StrictStr
from clipped.config.schema import BaseSchemaModel
from clipped.types.ref_or_obj import RefField


class BucketConnection(BaseSchemaModel):
    _IDENTIFIER = "bucket"

    kind: Optional[
        StrictStr
    ]  # TODO: Remove once the kind is not set in the compiler, because the schema is converted to a `dict`
    bucket: StrictStr

    def patch(self, schema: "BucketConnection"):
        self.bucket = schema.bucket or self.bucket


class ClaimConnection(BaseSchemaModel):
    _IDENTIFIER = "volume_claim"

    kind: Optional[
        StrictStr
    ]  # TODO: Remove once the kind is not set in the compiler, because the schema is converted to a `dict`
    volume_claim: StrictStr = Field(alias="volumeClaim")
    mount_path: StrictStr = Field(alias="mountPath")
    read_only: Optional[bool] = Field(alias="readOnly")

    def patch(self, schema: "ClaimConnection"):  # type: ignore
        self.volume_claim = schema.volume_claim or self.volume_claim
        self.mount_path = schema.mount_path or self.mount_path
        self.read_only = schema.read_only or self.read_only


class HostPathConnection(BaseSchemaModel):
    _IDENTIFIER = "host_path"

    kind: Optional[
        StrictStr
    ]  # TODO: Remove once the kind is not set in the compiler, because the schema is converted to a `dict`
    host_path: StrictStr = Field(alias="hostPath")
    mount_path: StrictStr = Field(alias="mountPath")
    read_only: Optional[bool] = Field(alias="readOnly")

    def patch(self, schema: "HostPathConnection"):  # type: ignore
        self.host_path = schema.host_path or self.host_path
        self.mount_path = schema.mount_path or self.mount_path
        self.read_only = schema.read_only or self.read_only


class HostConnection(BaseSchemaModel):
    _IDENTIFIER = "host"

    kind: Optional[
        StrictStr
    ]  # TODO: Remove once the kind is not set in the compiler, because the schema is converted to a `dict`
    url: StrictStr
    insecure: Optional[bool]

    def patch(self, schema: "HostConnection"):  # type: ignore
        self.url = schema.url or self.url
        self.insecure = schema.insecure or self.insecure


class GitConnection(BaseSchemaModel):
    _IDENTIFIER = "git"

    kind: Optional[
        StrictStr
    ]  # TODO: Remove once the kind is not set in the compiler, because the schema is converted to a `dict`
    url: Optional[StrictStr]
    revision: Optional[StrictStr]
    flags: Optional[List[StrictStr]]

    def get_name(self):
        if self.url:
            return self.url.split("/")[-1].split(".")[0]
        return None

    def patch(self, schema: "GitConnection"):
        self.url = schema.url or self.url
        self.revision = schema.revision or self.revision
        self.flags = schema.flags or self.flags


def patch_git(schema: Dict, git_schema: GitConnection):
    if git_schema.url:
        setattr(schema, "url", git_schema.url)
    if git_schema.revision:
        setattr(schema, "revision", git_schema.revision)
    if git_schema.flags:
        setattr(schema, "flags", git_schema.flags)


ConnectionSchema = Union[
    BucketConnection,
    ClaimConnection,
    HostPathConnection,
    HostConnection,
    GitConnection,
    Dict,
    RefField,
]
