from enum import IntEnum, StrEnum, auto
from fastapi import status

class TaskStatus(StrEnum):
	created = auto()
	in_progress = auto()
	finished = auto()

class APIErrorSpecs(StrEnum):
	unknown_error = auto()
	not_found = auto()
	validation_error = auto()

class StatusCodeMap(IntEnum):
	unknown_error = status.HTTP_500_INTERNAL_SERVER_ERROR
	not_found = status.HTTP_404_NOT_FOUND
	validation_error = status.HTTP_422_UNPROCESSABLE_ENTITY

