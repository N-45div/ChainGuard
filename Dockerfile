FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and source files
COPY pyproject.toml .
COPY server.py .

# Install Python dependencies
RUN pip install requests mcp fastmcp trio

# Set environment variables for stdio mode
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Run the MCP server in stdio mode
CMD ["python", "server.py"]
