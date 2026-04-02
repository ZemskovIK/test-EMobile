from fastapi import FastAPI

app = FastAPI(title="Auth & RBAC System", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Auth system is running"}