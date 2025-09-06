#!/usr/bin/env python3
"""
Test script for ChainGuard MCP Server
Run this to test your MCP server functionality
"""

import requests
import json
import subprocess
import time

def test_http_server():
    """Test the HTTP version of the server"""
    print("🚀 Starting HTTP server test...")
    
    # Start HTTP server in background
    try:
        proc = subprocess.Popen(
            ["python", "http_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Test endpoints
        base_url = "http://localhost:8000"
        
        # Test health check
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.json()}")
        
        # Test Bitcoin analysis
        bitcoin_data = {
            "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        }
        response = requests.post(f"{base_url}/analyze/bitcoin", json=bitcoin_data)
        print(f"✅ Bitcoin analysis: {response.status_code}")
        
        # Test Ethereum analysis  
        ethereum_data = {
            "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        }
        response = requests.post(f"{base_url}/analyze/ethereum", json=ethereum_data)
        print(f"✅ Ethereum analysis: {response.status_code}")
        
        proc.terminate()
        print("🎉 HTTP server tests completed!")
        
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")

def test_mcp_stdio():
    """Test MCP server via stdio"""
    print("🔍 Testing MCP stdio server...")
    
    try:
        # Test tools list
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        proc = subprocess.Popen(
            ["python", "server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send request
        stdout, stderr = proc.communicate(
            input=json.dumps(mcp_request) + "\n",
            timeout=10
        )
        
        if stdout:
            print(f"✅ MCP Response: {stdout[:200]}...")
        else:
            print(f"❌ No response. Error: {stderr}")
            
    except Exception as e:
        print(f"❌ MCP stdio test failed: {e}")

if __name__ == "__main__":
    print("🛡️  ChainGuard MCP Server Test Suite")
    print("=" * 50)
    
    # Test HTTP mode
    test_http_server()
    print()
    
    # Test MCP stdio mode
    test_mcp_stdio()
    
    print("\n🎯 For Claude Desktop integration:")
    print("Add this to your Claude Desktop MCP config:")
    print(json.dumps({
        "mcpServers": {
            "chainguard": {
                "command": "docker",
                "args": ["exec", "-i", "chainguard-mcp-server", "python", "server.py"]
            }
        }
    }, indent=2))
