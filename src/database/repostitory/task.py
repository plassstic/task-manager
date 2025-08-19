import uuid
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.model.task import TaskDBM


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def create(self, name: str, description: str | None = None) -> TaskDBM:
        task = TaskDBM(name=name, description=description)

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get(self, task_id: uuid.UUID) -> TaskDBM | None:
        return await self.session.get(TaskDBM, task_id)

    async def get_paginated(
        self, page: int = 1, page_size: int = 5
    ) -> list[TaskDBM] | None:
        query = sa.select(TaskDBM).offset((page - 1) * page_size).limit(page_size)

        return (await self.session.execute(query)).scalars().all()

    async def update(
        self, task_id: uuid.UUID, **kwargs: dict[str, str]
    ) -> TaskDBM | None:
        task = await self.get(task_id=task_id)

        for attr, val in kwargs.items():
            setattr(task, attr, val)

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete(self, task_id: uuid.UUID) -> bool:
        return (
            await self.session.execute(
                sa
                .delete(TaskDBM)
                .where(TaskDBM.id == task_id)
                .returning(TaskDBM.id)
            )
        ).scalar_one_or_none() is not None