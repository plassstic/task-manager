from dataclasses import dataclass
from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from loguru import logger


@dataclass
class AppSettings:
	REDIS_PASSWORD: str
	POSTGRES_PASSWORD: str

	DOCKER_MODE: bool = False

	DB_MAX_CONNECTIONS: int = 10

	REDIS_PORT: str = "6379"

	POSTGRES_USER: str = "testdb"
	POSTGRES_PORT: str = "5432"
	POSTGRES_DB: str = "testdb"
	POSTGRES_ECHO: bool = False
	DB_SCHEMA: str = "taskmgr_plstc"

	UVICORN_PORT: int = 8000
 
	def __init__(self):
		load_dotenv()

		for attr, _type in self.__annotations__.items():
			try:
				var = getenv(attr, None)

				if var is None:
					if "secret" in attr.lower() or "pass" in attr.lower():
						logger.error("[secret not configured, generated] {}=Redacted", attr)
					else:
						logger.warning("[default] {}={}", attr, self.__class__.__dict__[attr])
					continue

				var = "true" in var.lower() if _type is bool else _type(var)
				setattr(self, attr, var)

				if any(_ in attr.lower() for _ in ("secret", "pass", "token")):
					logger.success(
						"[secret] {}={}",
						attr,
						var[: len(var) // 4] + ("*" * 3 * (len(var) // 4))
						if "token" in attr.lower()
						else "Redacted",
					)
				else:
					logger.info("{}={}", attr, var)
			except Exception as exc:
				logger.error(
					"failed to load attr {} type {} exc {}",
					attr,
					_type,
					str(exc),
				)

	@property
	def postgres_async_uri(self):
		return "postgresql+asyncpg://{}:{}@{}:{}/".format(
			self.POSTGRES_USER,
			self.POSTGRES_PASSWORD,
			"pg" if self.DOCKER_MODE else "localhost",
			self.POSTGRES_PORT,
		)

	@property
	def postgres_sync_uri(self):
		return self.postgres_async_uri.replace("+asyncpg", "")

	def test_api_base(self, path):
		return f"http://localhost:{self.UVICORN_PORT}/api{path}"

@lru_cache
def get_cached_settings() -> AppSettings:
	return AppSettings()