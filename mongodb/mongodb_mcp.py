# mongodb_mcp.py - MongoDB-specific MCP Server
import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, List

import orjson as json
from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.fastmcp.resources.templates import ResourceTemplate
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@dataclass
class MongoDBContext:
    pass


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[MongoDBContext]:
    # Create a MongoDB client using AsyncIOMotorClient
    motor_client = None
    # Create the app context
    ctx = None

    try:
        yield ctx
    finally:
        # Close the MongoDB client when the app shuts down
        motor_client.close()


# Create an MCP server with the lifespan context manager
mcp = FastMCP("MongoDB-MCP", lifespan=lifespan)

# Implement tool to insert documents

# Implement resource to query documents from collection

# Implement tool to delete documents that match a search query

# Implement tool to 

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse", port=8000)
