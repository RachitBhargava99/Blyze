from fastapi import APIRouter

from api.users.routes import router as user_router

api_router = APIRouter()

api_router.include_router(router=user_router, prefix='/user')




