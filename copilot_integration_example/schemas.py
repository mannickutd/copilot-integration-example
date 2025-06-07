from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID


class ClientBase(BaseModel):
    name: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class NetworkBase(BaseModel):
    ipv4: Optional[str] = None


class NetworkCreate(NetworkBase):
    pass


class Network(NetworkBase):
    id: int

    model_config = ConfigDict(from_attributes=True)