from fastapi import FastAPI
from sqlmodel import SQLModel

app = FastAPI()

app.title("API EFI")

app.include_router(router)

app.middleware()
