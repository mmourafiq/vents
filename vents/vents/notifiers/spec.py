from datetime import datetime
from typing import Dict, Optional

from clipped.config.schema import BaseSchemaModel
from clipped.types import Uri


class NotificationSpec(BaseSchemaModel):
    title: str
    description: str
    details: str
    fallback: Optional[str]
    context: Optional[Dict]
    url: Optional[Uri]
    color: Optional[str]
    ts: Optional[datetime]
