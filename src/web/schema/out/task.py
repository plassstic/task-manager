import uuid
from pydantic import Field

from src.utility import TaskStatus
from .base import BaseSO


class TaskSO(BaseSO):
	id: uuid.UUID           = Field(description="*UUID задачи", examples=[uuid.uuid4()])
	name: str               = Field(description="*Имя задачи", examples=["Сдать курсач"])
	description: str | None = Field(None, description="Описание задачи", examples=["Очень важно!"])
	status: TaskStatus      = Field(description="*Статус задачи", examples=[stat.name for stat in TaskStatus])