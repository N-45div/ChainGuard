# Running ChainGuard MCP Server with Docker

## Method 1: Using Docker Build & Run (Recommended)

### 1. Build the Docker Image
```bash
cd /home/divij/MessariMCP
docker build -t chainguard-mcp .
```

### 2. Run the MCP Server in stdio Mode
```bash
docker run -it --name chainguard-mcp-server chainguard-mcp
```

### 3. Interact with the Server
Once running, you can send MCP protocol messages via stdin. Example:
```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
```

## Method 2: Using Docker Compose

### 1. Start the Service
```bash
docker-compose up --build
```

### 2. Attach to Running Container
```bash
docker exec -it chainguard-mcp-server /bin/bash
```

## Method 3: Interactive Testing Mode

### Run with Shell Access
```bash
docker run -it --entrypoint /bin/bash chainguard-mcp
# Inside container:
python server.py
```

## Method 4: Testing MCP Tools Directly

### Run Individual Tools
```bash
docker run -it chainguard-mcp python -c "
import asyncio
from server import analyze_bitcoin_address
result = asyncio.run(analyze_bitcoin_address('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'))
print(result)
"
```

## Useful Docker Commands

### View Logs
```bash
docker logs chainguard-mcp-server
```

### Stop Container
```bash
docker stop chainguard-mcp-server
```

### Remove Container
```bash
docker rm chainguard-mcp-server
```

### Clean Up
```bash
docker system prune -f
```

## Environment Variables

You can pass environment variables for API keys:
```bash
docker run -it \
  -e ETHERSCAN_API_KEY=your_key_here \
  -e HELIUS_API_KEY=your_key_here \
  --name chainguard-mcp-server \
  chainguard-mcp
```

## Troubleshooting

1. **Container exits immediately**: Check logs with `docker logs chainguard-mcp-server`
2. **Permission issues**: Ensure Docker daemon is running
3. **Build fails**: Check if all files are present in the directory
4. **stdio hanging**: This is normal - MCP servers wait for input via stdin/stdout protocol
