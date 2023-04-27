from typing import List, Optional

from clipped.config.schema import BaseSchemaModel
from pydantic import Field, StrictStr


class K8sResource(BaseSchemaModel):
    _IDENTIFIER = "k8s_resource"

    name: StrictStr
    mount_path: Optional[StrictStr] = Field(alias="mountPath")
    items: Optional[List[StrictStr]]
    default_mode: Optional[str] = Field(alias="defaultMode")
    is_requested: Optional[bool] = Field(alias="isRequested")
