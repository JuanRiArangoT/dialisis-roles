from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PermissionOutputDTO:
    permission_id: str
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime