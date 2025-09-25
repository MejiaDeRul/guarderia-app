from pydantic import BaseModel

class EnrollmentBase(BaseModel):
    child_id: int
    class_group_id: int


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentOut(EnrollmentBase):
    id: int
    class Config:
        from_attributes = True