from fastapi import APIRouter

from api.users.routes import router as user_router
from api.orgs.routes import router as org_router

api_router = APIRouter()

api_router.include_router(router=user_router, prefix='/user')
api_router.include_router(router=org_router, prefix='/orgs')
