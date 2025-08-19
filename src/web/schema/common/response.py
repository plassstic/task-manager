from pydantic import BaseModel, model_validator
from typing import Any

class ErrorSO(BaseModel):
	error: str = "unknown"
	error_description: str | None = None
	error_data: dict[str, Any] = {}

class ResponseSO[T: BaseModel](BaseModel):
	payload: T | None = None
	error: ErrorSO | None = None