from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from src.database.model import BaseDBM


class BaseSO(BaseModel):
	class Config:
		from_attributes = True

	created_at: datetime
	updated_at: datetime

	@classmethod
	def from_dbm(cls, db_model: BaseDBM) -> BaseSO:
		return cls(
			**db_model._to_dict()
		)