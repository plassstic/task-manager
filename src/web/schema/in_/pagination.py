from pydantic import BaseModel, Field


class PaginationSI(BaseModel):
	page: int = Field(1, ge=1, description="Порядковый № страницы (>= 1)")
	page_size: int = Field(10, ge=1, description="Кол-во задач на одной странице (>= 1)")