from typing import List, Optional

from clipped.compact.pydantic import Field, StrictStr
from clipped.config.schema import BaseSchemaModel


class ConnectionResource(BaseSchemaModel):
    _IDENTIFIER = "connection_resource"

    name: StrictStr
    mount_path: Optional[StrictStr] = Field(alias="mountPath")
    host_path: Optional[StrictStr] = Field(alias="hostPath")
    items: Optional[List[StrictStr]]
    default_mode: Optional[str] = Field(alias="defaultMode")
    is_requested: Optional[bool] = Field(alias="isRequested")
