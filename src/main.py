from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps.attendances import router as attendances_router
from src.apps.auth import router as auth_router
from src.apps.classrooms import router as classrooms_router
from src.apps.students import router as students_router
from src.apps.teachers import router as teachers_router
from src.config import Settings
from src.database.base import Base
from src.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teachers_router.router)
app.include_router(classrooms_router.router)
app.include_router(auth_router.router)
app.include_router(students_router.router)
app.include_router(attendances_router.router)
