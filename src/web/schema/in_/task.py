from typing import Optional

from pydantic import BaseModel, Field

from src.utility import TaskStatus


class TaskUpdateSI(BaseModel):
	name: Optional[str] = Field(None, description="name")
	description: Optional[str] = Field(None, description="desc")
	status: Optional[TaskStatus] = Field(None, description="status")


class TaskCreateSI(BaseModel):
	name: str
	description: str | None
