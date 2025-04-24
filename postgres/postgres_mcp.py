# postgres_mcp.py - PostgreSQL-specific MCP Server with SQLAlchemy
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import orjson as json
from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@dataclass
class PostgresContext:
    engine: AsyncEngine
    session_maker: async_sessionmaker[AsyncSession]


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[PostgresContext]:
    # Create async SQLAlchemy engine and session
    # Note: postgresql+asyncpg:// for async support
    connection_string = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    # Create async engine
    engine = create_async_engine(
        connection_string,
        echo=False,  # Set to True for query logging
        pool_pre_ping=True,  # Verify connections before use
        pool_size=5,
        max_overflow=10,
    )

    # Create async session maker
    session_maker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    # Create app context
    ctx = PostgresContext(engine=engine, session_maker=session_maker)

    try:
        yield ctx
    finally:
        # Close all connections in the pool
        await engine.dispose()


# Create a separate MCP server for PostgreSQL
mcp = FastMCP("PostgreSQL-MCP", lifespan=lifespan)

# Implement resources to get all contents of a table

# Implement tools to execute SQL queries

if __name__ == "__main__":
    # Initialize and run the server on a different port
    mcp.run(transport="sse", port=8003)
