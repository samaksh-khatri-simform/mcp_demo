# tavily_mcp.py - Tavily-specific MCP Server
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from os import getenv
from typing import Literal

import orjson as json
from loguru import logger
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from tavily import AsyncTavilyClient


@dataclass
class TavilyContext:
    tavily_client: AsyncTavilyClient


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[TavilyContext]:
    # Create a Tavily client
    tavily_api_key = getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("Tavily API Key not configured")
    tavily_client = AsyncTavilyClient(api_key=tavily_api_key)
    # Create the app context
    ctx = TavilyContext(tavily_client=tavily_client)

    try:
        yield ctx
    finally:
        # No cleanup needed for Tavily client
        pass


# Create a separate MCP server for Tavily
mcp = FastMCP("Tavily-MCP", lifespan=lifespan)


@logger.catch
@mcp.tool(name="tavily_search")
async def tavily_search(
    ctx: Context,
    query: str,
    search_depth: Literal["basic", "advanced"] = "basic",
    topic: Literal["general", "news", "finance"] = "general",
    time_range: Literal["day", "week", "month", "year"] = None,
    days: int = 7,
    max_results: int = 5,
    timeout: int = 120,
) -> dict:
    """
    Search the web using Tavily API.
    """
    try:
        tavily_client: AsyncTavilyClient = (
            ctx.request_context.lifespan_context.tavily_client
        )
        response = await tavily_client.search(
            query=query,
            search_depth=search_depth,
            topic=topic,
            time_range=time_range,
            days=days,
            max_results=max_results,
            timeout=timeout,
        )
        if response:
            return json.dumps(response)
        return "No information found"
    except ToolError as e:
        return f"Error while executing tool: {e}"
    except Exception as e:
        return f"Error: {e}"


@mcp.resource("tavily://tavily-info")
async def get_tavily_info() -> str:
    """Get information about the Tavily service"""
    return "Tavily is a web search API service that allows you to search the web programmatically."


@mcp.resource("roots://list")
async def list_roots():
    return {
        "roots": [
            {
                "uri": "file:///home/samaksh/Desktop/Projects/mcp_demo/",
                "name": "MCP Demo Repository",
            },
        ]
    }


@mcp.prompt()
async def get_tavily_prompt(message: str) -> str:
    return f"Tavily Search Assistant: {message}"


if __name__ == "__main__":
    # Initialize and run the server on a different port
    mcp.run(transport="sse")
