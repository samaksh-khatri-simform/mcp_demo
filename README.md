# Installation

1. Create a virtual environment using `uv` and install dependencies
   ```bash
   uv venv --python 3.11.10
   source ./.venv/bin/activate
   uv sync
   ```

2. Run the sample MCP server
   ```bash
   uv run tavily/tavily_mcp_server.py
   ```

3. Run the sample client side code in new terminal
   ```bash
   uv run client.py
   ```

# Docker Images

1. PostgreSQL
   ```bash
   docker run -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres
   ```

2. MongoDB
   ```bash
    docker run -p 27017:27017 -d mongo
   ```

3. Qdrant
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

# Documentation

1. Model Context Protocol Python SDK - https://github.com/modelcontextprotocol/python-sdk
2. Qdrant Python SDK - https://python-client.qdrant.tech/
3. MotorIO - https://motor.readthedocs.io/en/stable/
4. SQLAlchemy for PostgreSQL - https://docs.sqlalchemy.org/en/20/dialects/postgresql.html