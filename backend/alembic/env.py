import os
import sys
from logging.config import fileConfig
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add backend parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.models import Base


root_env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
test_env_path = os.path.join(os.path.dirname(__file__), "..", "test", ".env")
load_dotenv(root_env_path)
load_dotenv(test_env_path)


def get_url() -> str:
    explicit_url = os.getenv("ALEMBIC_DATABASE_URL")
    if explicit_url:
        return explicit_url

    target_db = os.getenv("ALEMBIC_TARGET_DB", "production").strip().lower()
    if target_db not in {"production", "test"}:
        raise RuntimeError("ALEMBIC_TARGET_DB must be either 'production' or 'test'.")

    production_url = os.getenv("SQLALCHEMY_PRODUCTION_DATABASE_URL") or os.getenv(
        "SQLALCHEMY_DATABASE_URL"
    )
    if target_db == "production":
        if not production_url:
            raise RuntimeError(
                "Set SQLALCHEMY_PRODUCTION_DATABASE_URL or SQLALCHEMY_DATABASE_URL for production Alembic migrations."
            )
        return production_url

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    if not all([user, password, host, port, name]):
        raise RuntimeError(
            "For test Alembic migrations, set DB_USER/DB_PASSWORD/DB_HOST/DB_PORT/DB_NAME."
        )
    safe_password = quote_plus(password)
    return f"postgresql+psycopg2://{user}:{safe_password}@{host}:{port}/{name}"


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Align Alembic with the app's DB connection using env vars
config.set_main_option("sqlalchemy.url", get_url())

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
