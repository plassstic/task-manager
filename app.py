from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.responses import JSONResponse

from src.database import close_db, init_db
from src.web.api import main_router


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

@app.get("/health")
async def _():
	return JSONResponse({"status": "ok"})