from pydantic import BaseModel, EmailStr


class TeacherBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class TeacherCreate(TeacherBase):
    password: str


class Teacher(TeacherBase):
    id: int

    # classrooms: list[Classroom] = []

    class Config:
        orm_mode = True
