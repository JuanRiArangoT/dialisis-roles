from pydantic import BaseModel


class CreateRoleRequest(BaseModel):
    name: str
    description: str | None = None