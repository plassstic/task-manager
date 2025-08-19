import uuid

from sqlalchemy import UUID, func
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.database.model import BaseDBM
from src.utility import TaskStatus


class TaskDBM(BaseDBM):
	__tablename__ = "tasks"

	id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True),
		primary_key=True,
		insert_default=uuid.uuid4,
		server_default=func.gen_random_uuid(),
	)

	name: Mapped[str] = mapped_column(
		nullable=False,
	)

	description: Mapped[str] = mapped_column(
		nullable=True
	)

	status: Mapped[TaskStatus] = mapped_column(
		nullable=False,
		default=TaskStatus.created.name
	)
