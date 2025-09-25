from pydantic import BaseModel

class ChildBase(BaseModel):
    first_name: str
    last_name: str
    parent_id: int


class ChildCreate(ChildBase):
    pass


class ChildOut(ChildBase):
    id: int
    class Config:
        from_attributes = True