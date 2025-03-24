from fastapi import APIRouter
from app.api.endpoints import journals, therapists

api_router = APIRouter()
api_router.include_router(journals.router, tags=["journals"])
api_router.include_router(therapists.router, tags=["therapists"])
