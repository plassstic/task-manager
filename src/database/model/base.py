import pprint

from datetime import datetime

from sqlalchemy import DateTime, MetaData, func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column

from src.utility import get_cached_settings


metadata = MetaData(schema=get_cached_settings().DB_SCHEMA)


class BaseDBM(DeclarativeBase):
	__abstract__ = True

	metadata = metadata

	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

	def _to_dict(self):
		return {field.name: getattr(self, field.name) for field in self.__table__.c}

	def __str__(self):
		return "{}: {}".format(self.__class__.__name__, pprint.pformat(self._to_dict()))
