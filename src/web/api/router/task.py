import uuid

import fastapi.requests
from fastapi import APIRouter

from src.database.service import TaskService
from src.web.schema.common import ResponseSO
from src.web.schema.in_ import PaginationSI, TaskCreateSI, TaskUpdateSI
from src.web.schema.out import TaskSO

router = APIRouter()


@router.get("/")
async def _(
	*,
	request: fastapi.requests.Request,
	response: fastapi.responses.Response,
	pagination: PaginationSI = fastapi.Query(PaginationSI())
) -> ResponseSO[list[TaskSO]]:
	tasks = await TaskService.get_paginated(**pagination.model_dump())
	return ResponseSO[list[TaskSO]](payload=tasks)

@router.get("/{task_id}")
async def _(
	*,
	request: fastapi.requests.Request,
	response: fastapi.responses.Response,
	task_id: uuid.UUID
) -> ResponseSO[TaskSO]:
	task = await TaskService.get(task_id=task_id)
	return ResponseSO[TaskSO](payload=task)

@router.post("/")
async def _(
	*,
	request: fastapi.requests.Request,
	response: fastapi.responses.Response,
	schema_in: TaskCreateSI = fastapi.Body(),
) -> ResponseSO[TaskSO]:
	task = await TaskService.create(schema_in=schema_in)
	return ResponseSO[TaskSO](payload=task)

@router.patch("/{task_id}")
async def _(
	*,
	request: fastapi.requests.Request,
	response: fastapi.responses.Response,
	task_id: uuid.UUID,
	schema_in: TaskUpdateSI = fastapi.Body()
) -> ResponseSO[TaskSO]:
	task = await TaskService.update(task_id=task_id, schema_in=schema_in)
	return ResponseSO[TaskSO](payload=task)

@router.delete("/{task_id}")
async def _(
	*,
	request: fastapi.requests.Request,
	response: fastapi.responses.Response,
	task_id: uuid.UUID,
) -> ResponseSO[bool]:
	await TaskService.delete(task_id=task_id)
	return ResponseSO[bool](payload=True)