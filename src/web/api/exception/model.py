from typing import Any

import fastapi.security

from src.utility import APIErrorSpecs
from src.web.schema.common import ErrorSO


class APIException(fastapi.exceptions.HTTPException):
    def __init__(
            self,
            *,
            status_code: int = fastapi.status.HTTP_400_BAD_REQUEST,
            error_code: str | None = APIErrorSpecs.unknown_error,
            error_description: str | None = None,
            error_data: dict[str, Any] = {}
    ):
        self.status_code = status_code

        self.error = error_code
        self.error_description = error_description
        self.error_data = error_data

        self.error_so = ErrorSO(
            error=self.error,
            error_description=self.error_description,
            error_data=self.error_data
        )

        super().__init__(
            status_code=self.status_code,
            detail=self.error_so.model_dump(mode="json")
        )