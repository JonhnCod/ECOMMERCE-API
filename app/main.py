from fastapi import FastAPI
from app.routers import usuarios, auth

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(auth.auth_router)


