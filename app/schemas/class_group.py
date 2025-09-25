from pydantic import BaseModel

class ClassGroupBase(BaseModel):
    name: str
    teacher_id: int | None = None


class ClassGroupCreate(ClassGroupBase):
    pass


class ClassGroupOut(ClassGroupBase):
    id: int
    class Config:
        from_attributes = True