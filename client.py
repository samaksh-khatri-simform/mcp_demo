#!/usr/bin/env python3
# client.py
import asyncio
from textwrap import dedent
from typing import Any

import mcp.types as types

# from typing import Any, Dict, List
from agno.agent.agent import Agent
from agno.tools.mcp import MCPTools
from mcp import ClientSession

# from mcp.client import Client, Resource, Tool
from mcp.client.sse import sse_client
from mcp.shared.context import RequestContext

from llm import model


async def sampling_callback(
    context: RequestContext["ClientSession", Any],
    params: types.CreateMessageRequestParams,
) -> types.CreateMessageResult | types.ErrorData:
    messages = params.messages
    system_prompt = params.systemPrompt
    model.system_prompt = system_prompt
    response = await model.ainvoke(messages=messages)
    return types.CreateMessageResult(
        role=response.choices[0].message.role,
        content=response.choices[0].message.content,
        model=model.id,
    )


async def main(message):
    # Create an MCP client connecting to the local server
    # By default, MCP server runs on port 8000
    async with sse_client("http://localhost:8000/sse", timeout=120) as (read, write):
        async with ClientSession(
            read_stream=read, write_stream=write, sampling_callback=sampling_callback
        ) as session:
            await session.initialize()
            async with MCPTools(session=session) as mcp_tool:
                agent = Agent(
                    model=model,
                    tools=[mcp_tool],
                    # Change the below instructions as per your implementation
                    instructions=dedent("""\
                            You are a research assistant that helps users find information online.
                            
                            When given a query:
                            1. Use the tavily_search tool to gather relevant information
                            2. Analyze and synthesize the search results
                            3. Create a comprehensive report with the following sections:
                            - Introduction: Brief overview of the topic
                            - Key Findings: Main points discovered from research
                            - Details: In-depth information organized by subtopics
                            - Conclusion: Summary of findings
                            
                            Format your report using proper Markdown, including:
                            - Headings (# for main headings, ## for subheadings)
                            - Lists (bullet or numbered as appropriate)
                            - Emphasis (**bold** for important terms)
                            - Links to sources when available
                            
                            Always cite your sources at the end of the report.
                            Use the tavily-info when asked information about Tavily\
                        """),
                    markdown=True,
                    show_tool_calls=True,
                )
                # response = await agent.
                await agent.aprint_response(message, stream=True)


if __name__ == "__main__":
    # Run the main coroutine
    asyncio.run(
        main("Conduct an in depth research about Microsoft's new Majorana particles")
    )
