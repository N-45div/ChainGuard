# 🛡️ ChainGuard - Multi-Chain Crime Detection MCP Server

**Aya AI Hackathon Taipei Edition Submission**

ChainGuard is a comprehensive blockchain crime detection system built as an MCP (Model Context Protocol) server. It provides real-time analysis and risk assessment across Bitcoin, Ethereum, Hedera, and Solana networks to identify suspicious activities, fraud patterns, and criminal behavior.

---

## 🎯 Features

### Multi-Chain Analysis
- **Bitcoin**: Address analysis, transaction tracking, suspicious pattern detection
- **Ethereum**: Smart contract analysis, rug pull detection, address investigation  
- **Hedera**: Account analysis, transaction monitoring via Mirror Node API
- **Solana**: Wallet analysis, pump & dump detection, token investigation

### Crime Detection Capabilities
- **Risk Scoring**: Automated risk assessment (0-100 scale)
- **Pattern Recognition**: High-frequency transactions, large value transfers
- **Cross-Chain Correlation**: Link suspicious activities across blockchains
- **Real-Time Analysis**: Live blockchain data integration
- **Comprehensive Reports**: Multi-chain crime analysis reports

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
# Pull and run the MCP server
docker run -it divij/chainguard-mcp:latest

# Send MCP protocol messages
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}
{"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}
{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
```

### Option 2: Local Setup
```bash
git clone https://github.com/yourusername/chainguard-mcp.git
cd chainguard-mcp
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
```

### Option 3: Claude Desktop Integration
Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "chainguard": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "divij/chainguard-mcp:latest"]
    }
  }
}
```

---

## 🔧 Available Tools

### Bitcoin Analysis
- `analyze_bitcoin_address` - Comprehensive address risk assessment
- `track_bitcoin_transaction` - Transaction pattern analysis

### Ethereum Investigation
- `analyze_ethereum_address` - Smart contract and wallet analysis
- `detect_ethereum_rug_pull` - Rug pull pattern detection

### Hedera Monitoring
- `analyze_hedera_account` - Account activity analysis
- `track_hedera_transaction` - Transaction monitoring

### Solana Detection
- `analyze_solana_address` - Wallet risk assessment
- `detect_solana_pump_dump` - Pump & dump scheme detection

### Cross-Chain Reports
- `generate_crime_report` - Comprehensive multi-chain analysis

---

## 🧪 Testing

### Test MCP Functionality
```bash
python test_mcp.py
```

### Example Analysis
```bash
# Analyze Satoshi's Genesis address
{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "analyze_bitcoin_address", "arguments": {"address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"}}}
```

---

## 🏗️ Architecture

- **MCP Protocol**: Standard Model Context Protocol implementation
- **Multi-Chain APIs**: BlockCypher, Etherscan, Hedera Mirror Node, Helius
- **Crime Detection**: Custom algorithms for pattern recognition
- **Docker Ready**: Containerized for easy deployment
- **Claude Desktop**: Native integration support

---

## 🎪 Hackathon Submission

### Problem Solved
Blockchain crime detection is fragmented across different tools and chains. ChainGuard provides a unified, AI-accessible interface for comprehensive crime analysis.

### Innovation
- First MCP server for blockchain crime detection
- Cross-chain correlation analysis
- Natural language interface via Claude Desktop
- Real-time risk scoring algorithms

### Technical Excellence
- Professional MCP implementation
- Docker containerization
- Comprehensive test suite
- Multi-platform deployment ready

---

## 📊 Demo Results

**Bitcoin Genesis Address Analysis:**
- Balance: 104.32 BTC (~$4.7M)
- Risk Score: 30/100 (moderate)
- Transactions: 51,296
- Status: High frequency activity detected

---

## 🔑 API Keys (Optional)

For enhanced functionality, add API keys:
- `ETHERSCAN_API_KEY` - Ethereum analysis
- `HELIUS_API_KEY` - Solana analysis
- Bitcoin and Hedera work without keys (public APIs)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🏆 Aya AI Hackathon

**Team**: Solo Developer  
**Category**: MCPs + DeFi Automation  
**Submission Date**: September 2025  
**Demo**: Available via Docker and Claude Desktop integration
