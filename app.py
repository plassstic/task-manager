from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.database import close_db, init_db
from src.web.api import main_router
from src.web.api.exception import apply_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
	await init_db()

	yield

	await close_db()


app = FastAPI(lifespan=lifespan)
app.include_router(
	main_router,
	prefix="/api"
)
apply_exception_handler(app)


@app.get("/health")
async def _():
	return JSONResponse({"status": "ok"})