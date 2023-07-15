from sqlalchemy import Column, Date, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.database.session import Base


class Attendance(Base):
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    attended = Column(Boolean)
    student_id = Column(Integer, ForeignKey("students.id"))
    classroom_id = Column(Integer, ForeignKey("classrooms.id"))

    student = relationship("Student", back_populates="attendances")
    classroom = relationship("Classroom", back_populates="attendances")

    def __str__(self):
        return self.fecha.strftime('%d/%m/%Y')
