from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.session import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True )
    password = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    classrooms = relationship("Classroom", back_populates="teacher")
