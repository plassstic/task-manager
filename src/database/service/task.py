import uuid

from src.database import async_database_context
from src.database.repostitory import TaskRepository
from src.utility import APIErrorSpecs
from src.web.api.exception import APIException
from src.web.schema.in_ import TaskCreateSI, TaskUpdateSI
from src.web.schema.out import TaskSO


class TaskService:
	@staticmethod
	async def create(schema_in: TaskCreateSI) -> TaskSO:
		async with async_database_context() as session:
			repository = TaskRepository(session=session)
			task = await repository.create(**schema_in.model_dump(exclude_unset=True))
			return TaskSO.from_dbm(db_model=task)

	@staticmethod
	async def update(task_id: uuid.UUID, schema_in: TaskUpdateSI) -> TaskSO:
		async with async_database_context() as session:
			repository = TaskRepository(session=session)
			task = await repository.update(
				task_id=task_id, **schema_in.model_dump(exclude_none=True)
			)
			if task is None:
				raise APIException(
						status_code=404,
						error_code=APIErrorSpecs.not_found,
						error_description="Task with given UUID was not found"
				)
			return TaskSO.from_dbm(db_model=task)

	@staticmethod
	async def get(task_id: uuid.UUID) -> TaskSO:
		async with async_database_context() as session:
			repository = TaskRepository(session=session)
			task = await repository.get(task_id=task_id)
			if task is None:
				raise APIException(
					status_code=404,
					error_code=APIErrorSpecs.not_found,
					error_description="Task with given UUID was not found",
				)
			return TaskSO.from_dbm(db_model=task)

	@staticmethod
	async def get_paginated(page: int, page_size: int) -> list[TaskSO]:
		async with async_database_context() as session:
			repository = TaskRepository(session=session)
			tasks = await repository.get_paginated(page=page, page_size=page_size)
			return [TaskSO.from_dbm(db_model=task) for task in tasks]

	@staticmethod
	async def delete(task_id: uuid.UUID):
		async with async_database_context() as session:
			repository = TaskRepository(session=session)
			deleted = await repository.delete(task_id=task_id)
			if not deleted:
				raise APIException(
					status_code=404,
					error_code=APIErrorSpecs.not_found,
					error_description="Task with given UUID was not found",
				)