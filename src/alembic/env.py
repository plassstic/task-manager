from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool, text

from alembic import context

from src.config import get_cached_settings
from src.database.model import BaseDBM

config = context.config
if config.config_file_name is not None:
	fileConfig(config.config_file_name)
target_metadata = BaseDBM.metadata

def create_schema_if_not_exists(connection):
	schema_name = get_cached_settings().DB_SCHEMA
	connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
	connection.commit()

config.set_main_option("sqlalchemy.url", get_cached_settings().postgres_sync_uri)

def run_migrations_offline() -> None:
	url = config.get_main_option("sqlalchemy.url")

	engine = engine_from_config(
		{"sqlalchemy.url": url},
		prefix="sqlalchemy.",
		poolclass=pool.NullPool,
	)

	with engine.connect() as connection:
		create_schema_if_not_exists(connection)

	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		dialect_opts={"paramstyle": "named"},
	)

	with context.begin_transaction():
		context.run_migrations()


def run_migrations_online() -> None:
	connectable = engine_from_config(
		config.get_section(config.config_ini_section, {}),
		prefix="sqlalchemy.",
		poolclass=pool.NullPool,
	)

	with connectable.connect() as connection:
		create_schema_if_not_exists(connection)

		context.configure(
			connection=connection, target_metadata=target_metadata
		)

		with context.begin_transaction():
			context.run_migrations()


if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()
