from pydantic import BaseModel

from src.apps.students.schemas import StudentReadNested


class ClassroomBase(BaseModel):
    name: str


class ClassroomCreate(ClassroomBase):
    pass


class Classroom(ClassroomBase):
    id: str
    teacher_id: str
    students: list[StudentReadNested] = []

    class Config:
        orm_mode = True
