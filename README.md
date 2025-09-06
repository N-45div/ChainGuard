# ChainGuard - Multi-Chain Blockchain Crime Detection MCP Server

ChainGuard is an AI-powered MCP server that enables Claude Desktop to perform real-time blockchain crime detection and forensic analysis across Bitcoin, Ethereum, Hedera, and Solana networks through natural language conversations.

## 📋 Detailed Project Description

ChainGuard revolutionizes blockchain security by bringing sophisticated crime detection capabilities directly into AI assistants through the Model Context Protocol (MCP). This innovative solution addresses the growing need for accessible blockchain forensics in the DeFi ecosystem.

**Core Innovation:**
- **MCP Integration**: First-of-its-kind blockchain crime detection MCP server
- **Multi-Chain Support**: Unified analysis across 4 major blockchain networks
- **Natural Language Interface**: Complex blockchain analysis through simple conversations
- **Real-Time Detection**: Live monitoring and analysis of suspicious activities

**Technical Architecture:**
- Built on Cloudflare Workers for global scalability and low latency
- Implements MCP Streamable HTTP transport protocol
- Integrates with multiple blockchain APIs (Etherscan, Helius, BlockCypher, Hedera Mirror Node)
- Advanced pattern recognition algorithms for crime detection
- Comprehensive risk scoring and reputation systems

**Use Cases:**
- DeFi protocol security auditing
- Cryptocurrency exchange compliance
- Law enforcement blockchain investigations
- Individual wallet security assessment
- Cross-chain money laundering detection

🚀 **Live Server**: https://chainguard-mcp-server.ndivij2004.workers.dev/mcp

## Hackathon Focus: MCPs + DeFi Automation

This project directly addresses the hackathon's core theme by:
- **MCP Integration**: Full Model Context Protocol implementation for seamless AI assistant integration
- **DeFi Security**: Advanced crime detection algorithms for DeFi protocols and transactions
- **Cross-Chain Analysis**: Multi-blockchain support for comprehensive security coverage
- **Real-Time Detection**: Live analysis of suspicious activities and patterns

## 🔧 Quick Setup for Claude Desktop

### 1. Configure Claude Desktop

Add this configuration to your Claude Desktop settings (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "chainguard": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://chainguard-mcp-server.ndivij2004.workers.dev/mcp"
      ]
    }
  }
}
```

### 2. Restart Claude Desktop

After adding the configuration, restart Claude Desktop. The ChainGuard tools will appear under the 🔨 Tools section.

### 3. Start Analyzing

Try these example prompts:
- "Analyze Bitcoin address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa for suspicious activity"
- "Check Ethereum address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 for crime patterns"
- "Generate a comprehensive crime report for multiple addresses"

## 🛠️ Available Tools (9 Total)

| Tool | Description | Blockchain |
|------|-------------|------------|
| `analyze_bitcoin_address` | Bitcoin crime detection and transaction analysis | Bitcoin |
| `analyze_ethereum_address` | Ethereum address analysis and smart contract risks | Ethereum |
| `analyze_hedera_account` | Hedera account behavior and consensus analysis | Hedera |
| `analyze_solana_wallet` | Solana wallet analysis and token risk detection | Solana |
| `detect_rug_pull_ethereum` | Ethereum smart contract rug pull detection | Ethereum |
| `detect_pump_dump_solana` | Solana token pump & dump scheme detection | Solana |
| `analyze_cross_chain_activity` | Multi-chain suspicious activity correlation | All Chains |
| `generate_crime_report` | Comprehensive forensic reports | All Chains |
| `check_address_reputation` | Address reputation against crime databases | All Chains |

## 📦 Install Steps

### Prerequisites

- Node.js 18+ 
- npm or yarn package manager
- Cloudflare account (for deployment)
- API keys (optional but recommended):
  - [Etherscan API Key](https://etherscan.io/apis)
  - [Helius API Key](https://helius.xyz/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ndivij2004/MessariMCP.git
cd MessariMCP

# 2. Install dependencies
npm install

# 3. Copy environment variables template
cp .env.example .env

# 4. Build the project
npm run build

# 5. (Optional) Run locally for testing
npx wrangler dev
```

## 🔐 Environment Variables

The following environment variables are supported:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ETHERSCAN_API_KEY` | Etherscan API key for enhanced Ethereum data | No | `YourApiKeyToken` |
| `HELIUS_API_KEY` | Helius API key for enhanced Solana data | No | `demo` |
| `BLOCKCYPHER_API_KEY` | BlockCypher API key for Bitcoin data | No | Not used |

### Setting Environment Variables

**For Local Development:**
```bash
# Edit .env file
ETHERSCAN_API_KEY=your_etherscan_api_key_here
HELIUS_API_KEY=your_helius_api_key_here
```

**For Production (Cloudflare Workers):**
```bash
# Set secrets for production deployment
npx wrangler secret put ETHERSCAN_API_KEY
npx wrangler secret put HELIUS_API_KEY

# Verify secrets are set
npx wrangler secret list
```

### Deploy to Cloudflare Workers

```bash
# Deploy to production
npx wrangler deploy

# Check deployment status
npx wrangler tail
```

## 🔍 Key Features

### Multi-Chain Crime Detection
- **Bitcoin Analysis**: Transaction pattern analysis, mixer detection, and suspicious address identification
- **Ethereum Security**: Smart contract rug pull detection, MEV analysis, and gas anomaly detection  
- **Hedera Forensics**: Account behavior analysis and consensus timestamp verification
- **Solana Monitoring**: Pump & dump detection, wallet clustering, and program analysis

### Advanced Detection Algorithms
- **Pattern Recognition**: ML-powered detection of suspicious transaction patterns
- **Risk Scoring**: Comprehensive risk assessment with weighted factors
- **Cross-Chain Correlation**: Multi-blockchain activity pattern analysis
- **Real-Time Monitoring**: Live detection of emerging threats and schemes

## 💡 Usage Examples

### Basic Address Analysis
```
User: "Analyze Bitcoin address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa for suspicious activity"

ChainGuard Response:
- Transaction count: 1,000+
- Risk score: 15/100 (Low risk)
- Notable patterns: Genesis block address, high historical significance
- Recommendations: No suspicious activity detected
```

### Multi-Chain Investigation
```
User: "Generate a comprehensive crime report for these addresses: 
- Bitcoin: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
- Ethereum: 0x742d35Cc6634C0532925a3b8D4C9db4C7b5d8B3E"

ChainGuard Response:
- Cross-chain risk score: 75/100 (High risk)
- Suspicious patterns detected across both chains
- Timing correlations found in transaction patterns
- Recommended for further investigation
```

### DeFi Security Audit
```
User: "Check Ethereum contract 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984 for rug pull risks"

ChainGuard Response:
- Contract verification: ✅ Verified source code
- Ownership analysis: Decentralized governance
- Liquidity risks: Low
- Overall assessment: Safe for interaction
```

## ⚠️ Known Issues

1. **API Rate Limits**: 
   - Demo API keys have limited requests per minute
   - Solution: Use your own API keys for production usage

2. **Historical Data Limitations**:
   - Some blockchain APIs limit historical transaction depth
   - Impact: Older transactions may not be included in analysis

3. **Cross-Chain Timing**:
   - Different blockchain confirmation times affect real-time correlation
   - Mitigation: Analysis includes timestamp normalization

4. **False Positives**:
   - High-volume legitimate addresses may trigger risk alerts
   - Recommendation: Manual review for addresses with extreme activity

5. **Network Dependencies**:
   - Relies on external blockchain APIs (Etherscan, Helius, etc.)
   - Impact: Service availability depends on upstream providers

## 🔧 Troubleshooting

### Common Issues

**Claude Desktop not showing tools:**
- Ensure `mcp-remote` is installed: `npm install -g mcp-remote`
- Verify configuration in `claude_desktop_config.json`
- Restart Claude Desktop after configuration changes

**API errors:**
- Check if API keys are properly set
- Verify network connectivity
- Check API provider status pages

**Build failures:**
- Ensure Node.js 18+ is installed
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check TypeScript compilation: `npm run build`

## 🏆 Hackathon Achievements

- ✅ **Full MCP Implementation**: Complete Model Context Protocol server
- ✅ **Multi-Chain Support**: Bitcoin, Ethereum, Hedera, Solana integration
- ✅ **Production Ready**: Deployed on Cloudflare Workers with API key management
- ✅ **Natural Language Interface**: Seamless Claude Desktop integration
- ✅ **Advanced Analytics**: Sophisticated crime detection algorithms
- ✅ **Real-Time Analysis**: Live blockchain monitoring capabilities

## 📄 License

MIT License - See LICENSE file for details

## 👤 Project Information

- **Primary Contact**: N DIVIJ (@holaworked - Telegram)
- **Team**: Solo
- **Project Title**: ChainGuard - Multi-Chain Blockchain Crime Detection MCP Server

---
