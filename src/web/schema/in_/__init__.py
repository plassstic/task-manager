"""


Модуль входящих pydantic-схем


"""
from .pagination import PaginationSI
from .task import TaskCreateSI, TaskUpdateSI

__all__ = [
	# pagination
	"PaginationSI",
	# task
	"TaskUpdateSI",
	"TaskCreateSI"
]