from pydantic import BaseModel


class UpdateRoleRequest(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True