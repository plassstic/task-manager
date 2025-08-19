from fastapi import APIRouter

from .router import task_router

main_router = APIRouter()

main_router.include_router(router=task_router, prefix="/tasks", tags=["tasks"])

__all__ = ["main_router", "exception"]