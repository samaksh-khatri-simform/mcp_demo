# qdrant_mcp.py - Qdrant-specific MCP Server
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import orjson as json
from fastembed import TextEmbedding
from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models


@dataclass
class QdrantContext:
    qdrant_client: AsyncQdrantClient
    embedding_model: TextEmbedding


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[QdrantContext]:
    # Create a Qdrant client (defaults to localhost:6333)
    # Change url and api_key if connecting to a hosted Qdrant instance
    qdrant_client = AsyncQdrantClient(
        url="http://localhost:6333",
        # api_key="your-api-key-if-needed"
    )
    embedding_model = TextEmbedding("BAAI/bge-small-en-v1.5")
    # Create the app context
    ctx = QdrantContext(qdrant_client=qdrant_client, embedding_model=embedding_model)

    try:
        yield ctx
    finally:
        # Close the client connection
        await qdrant_client.close()


# Create a separate MCP server for Qdrant
mcp = FastMCP("Qdrant-MCP", lifespan=lifespan)


# Implement tools to search, insert and delete points

# Implement resource to get information about collections

if __name__ == "__main__":
    # Initialize and run the server on a different port
    mcp.run(transport="sse", port=8002)
