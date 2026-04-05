from fastapi import APIRouter, Depends
from app.dependencies import require_permission

router = APIRouter(prefix="/api/v1", tags=["mock-resources"])

@router.get("/reports")
async def get_reports(_=Depends(require_permission("reports", "read"))):
    return {"status": "ok", "data": [{"id": 1, "title": "Monthly Sales Report"}]}

@router.post("/analytics")
async def post_analytics(_=Depends(require_permission("analytics", "write"))):
    return {"status": "ok", "message": "Analytics data received"}