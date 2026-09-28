from dataclasses import dataclass
from datetime import datetime


@dataclass
class Role:
    id: str
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime