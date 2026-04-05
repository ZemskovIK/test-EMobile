from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, access_control, mock

app = FastAPI(title="Auth & RBAC System", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(access_control.router)
app.include_router(mock.router)

@app.get("/")
async def root():
    return {"message": "Auth & RBAC system is running"}