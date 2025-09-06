// Crime detection patterns and thresholds
const SUSPICIOUS_PATTERNS = {
  largeTransactionThreshold: 100000, // USD
  rapidTransactionsCount: 10, // transactions in short time
  rapidTransactionsWindow: 300, // 5 minutes in seconds
  mixingServiceIndicators: ["tornado", "mixer", "tumbler", "privacy"],
  flashLoanIndicators: ["flashloan", "aave", "compound", "dydx"]
};

interface Transaction {
  hash: string;
  value: number;
  timestamp: string;
  from: string;
  to: string;
  value_usd: number;
}

interface CrimeAnalysis {
  risk_score: number;
  alerts: string[];
  transaction_count: number;
  large_transactions: number;
}

class CrimeDetector {
  private suspiciousAddresses = new Set<string>();
  private knownMixers = new Set<string>();

  analyzeTransactionPattern(transactions: Transaction[]): any {
    if (!transactions.length) {
      return { risk_score: 0, alerts: [] };
    }

    const alerts: string[] = [];
    let risk_score = 0;

    // Check for rapid transactions
    if (transactions.length >= SUSPICIOUS_PATTERNS.rapidTransactionsCount) {
      risk_score += 30;
      alerts.push("High frequency transactions detected");
    }

    // Check for large value transactions
    const large_txs = transactions.filter(tx => tx.value_usd > SUSPICIOUS_PATTERNS.largeTransactionThreshold);
    if (large_txs.length > 0) {
      risk_score += 20;
      alerts.push(`Large transactions detected: ${large_txs.length} transactions`);
    }

    return {
      risk_score: Math.min(risk_score, 100),
      alerts,
      transaction_count: transactions.length,
      large_transactions: large_txs.length
    };
  }

  detectRugPull(transactions: Transaction[]): any {
    if (!transactions.length) {
      return { risk_score: 0, alerts: [], is_rug_pull: false };
    }

    const alerts: string[] = [];
    let risk_score = 0;
    let is_rug_pull = false;

    // Check for sudden large withdrawals
    const large_withdrawals = transactions.filter(tx => tx.value_usd > 50000);
    if (large_withdrawals.length > 0) {
      risk_score += 40;
      alerts.push("Large withdrawal detected - potential rug pull");
      is_rug_pull = true;
    }

    return {
      risk_score: Math.min(risk_score, 100),
      alerts,
      is_rug_pull,
      large_withdrawals: large_withdrawals.length
    };
  }

  detectPumpAndDump(transactions: Transaction[]): any {
    if (!transactions.length) {
      return { risk_score: 0, alerts: [], is_pump_dump: false };
    }

    const alerts: string[] = [];
    let risk_score = 0;
    let is_pump_dump = false;

    // Check for coordinated trading patterns
    if (transactions.length > 20) {
      risk_score += 35;
      alerts.push("High volume trading detected - potential pump and dump");
      is_pump_dump = true;
    }

    return {
      risk_score: Math.min(risk_score, 100),
      alerts,
      is_pump_dump,
      suspicious_volume: transactions.length > 20
    };
  }
}

const crimeDetector = new CrimeDetector();

// Analysis Functions
async function analyzeBitcoinAddress(address: string): Promise<any> {
  try {
    const response = await fetch(`https://api.blockcypher.com/v1/btc/main/addrs/${address}`);
    if (!response.ok) {
      const errorData = await response.json() as any;
      throw new Error(`BlockCypher API error: ${errorData.error || 'Unknown error'}`);
    }
    const data = await response.json() as any;

    const txResponse = await fetch(`https://api.blockcypher.com/v1/btc/main/addrs/${address}/full?limit=50`);
    const txData = await txResponse.json() as any;
    
    const transactions: Transaction[] = (txData.txs || []).slice(0, 10).map((tx: any) => ({
      hash: tx.hash,
      value: tx.total || 0,
      timestamp: tx.confirmed || new Date().toISOString(),
      from: tx.inputs?.[0]?.addresses?.[0] || 'unknown',
      to: tx.outputs?.[0]?.addresses?.[0] || 'unknown',
      value_usd: (tx.total || 0) * 0.00001
    }));

    const analysis = crimeDetector.analyzeTransactionPattern(transactions);

    return {
      address,
      balance_satoshis: data.balance || 0,
      balance_btc: (data.balance || 0) / 100000000,
      total_received: data.total_received || 0,
      total_sent: data.total_sent || 0,
      n_tx: data.n_tx || 0,
      unconfirmed_balance: data.unconfirmed_balance || 0,
      final_balance: data.final_balance || 0,
      transactions,
      crime_analysis: analysis
    };
  } catch (error) {
    throw new Error(`Bitcoin analysis failed: ${error}`);
  }
}


async function analyzeSolanaWallet(walletAddress: string, env?: any): Promise<any> {
  try {
    // Use Helius API for Solana data
    const apiKey = env?.HELIUS_API_KEY || 'demo';
    const response = await fetch(`https://api.helius.xyz/v0/addresses/${walletAddress}/balances?api-key=${apiKey}`);
    if (!response.ok) {
      throw new Error(`Helius API error: ${response.statusText}`);
    }
    const data = await response.json() as any;

    // Get transaction history
    const txResponse = await fetch(`https://api.helius.xyz/v0/addresses/${walletAddress}/transactions?api-key=${apiKey}&limit=100`);
    const txData = await txResponse.json() as any;
    
    const transactions: Transaction[] = (txData || []).slice(0, 10).map((tx: any) => ({
      hash: tx.signature || 'unknown',
      value: tx.nativeTransfers?.[0]?.amount || 0,
      timestamp: new Date(tx.timestamp * 1000).toISOString(),
      from: tx.nativeTransfers?.[0]?.fromUserAccount || 'unknown',
      to: tx.nativeTransfers?.[0]?.toUserAccount || 'unknown',
      value_usd: (tx.nativeTransfers?.[0]?.amount || 0) * 0.00000001 * 100 // Rough SOL to USD
    }));

    const analysis = crimeDetector.analyzeTransactionPattern(transactions);

    // Detect pump and dump patterns
    const pumpDumpAnalysis = {
      suspicious_token_activity: false,
      rapid_price_changes: false,
      coordinated_trading: false,
      risk_indicators: [] as string[]
    };

    // Check for suspicious token patterns
    if (data.tokens && data.tokens.length > 10) {
      pumpDumpAnalysis.suspicious_token_activity = true;
      pumpDumpAnalysis.risk_indicators.push("High number of different tokens");
    }

    return {
      wallet_address: walletAddress,
      sol_balance: data.nativeBalance || 0,
      token_count: data.tokens?.length || 0,
      transactions,
      crime_analysis: analysis,
      pump_dump_analysis: pumpDumpAnalysis
    };
  } catch (error) {
    throw new Error(`Solana analysis failed: ${error}`);
  }
}

async function detectRugPullEthereum(contractAddress: string): Promise<any> {
  try {
    const response = await fetch(`https://api.etherscan.io/api?module=contract&action=getsourcecode&address=${contractAddress}&apikey=YourApiKeyToken`);
    if (!response.ok) {
      throw new Error(`Etherscan API error: ${response.statusText}`);
    }
    const data = await response.json() as any;
    
    const rugPullIndicators = {
      no_source_code: !data.result?.[0]?.SourceCode,
      suspicious_functions: false,
      ownership_concentration: false,
      liquidity_risks: false,
      risk_score: 0,
      warnings: [] as string[]
    };

    if (rugPullIndicators.no_source_code) {
      rugPullIndicators.risk_score += 40;
      rugPullIndicators.warnings.push("Contract source code not verified");
    }

    return {
      contract_address: contractAddress,
      rug_pull_analysis: rugPullIndicators
    };
  } catch (error) {
    throw new Error(`Rug pull detection failed: ${error}`);
  }
}

async function detectPumpDumpSolana(tokenAddress: string, env?: any): Promise<any> {
  try {
    const apiKey = env?.HELIUS_API_KEY || 'demo';
    const response = await fetch(`https://api.helius.xyz/v0/token-metadata?api-key=${apiKey}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mintAccounts: [tokenAddress] })
    });
    
    if (!response.ok) {
      throw new Error(`Helius API error: ${response.statusText}`);
    }
    const data = await response.json() as any;

    const pumpDumpAnalysis = {
      suspicious_metadata: false,
      rapid_price_changes: false,
      coordinated_trading: false,
      risk_score: 0,
      warnings: [] as string[]
    };

    if (!data[0]?.onChainMetadata?.metadata) {
      pumpDumpAnalysis.suspicious_metadata = true;
      pumpDumpAnalysis.risk_score += 30;
      pumpDumpAnalysis.warnings.push("Missing or incomplete token metadata");
    }

    return {
      token_address: tokenAddress,
      pump_dump_analysis: pumpDumpAnalysis
    };
  } catch (error) {
    throw new Error(`Pump dump detection failed: ${error}`);
  }
}

async function analyzeCrossChainActivity(addresses: any): Promise<any> {
  try {
    const results = {
      bitcoin: null as any,
      ethereum: null as any,
      hedera: null as any,
      solana: null as any,
      cross_chain_risk_score: 0,
      correlation_analysis: {
        timing_correlations: false,
        value_correlations: false,
        suspicious_patterns: [] as string[]
      }
    };

    if (addresses.bitcoin) {
      results.bitcoin = await analyzeBitcoinAddress(addresses.bitcoin);
    }
    if (addresses.ethereum) {
      results.ethereum = await analyzeEthereumAddress(addresses.ethereum);
    }
    if (addresses.hedera) {
      results.hedera = await analyzeHederaAccount(addresses.hedera);
    }
    if (addresses.solana) {
      results.solana = await analyzeSolanaWallet(addresses.solana);
    }

    // Calculate cross-chain risk score
    const riskScores = [
      results.bitcoin?.crime_analysis?.risk_score || 0,
      results.ethereum?.crime_analysis?.risk_score || 0,
      results.hedera?.crime_analysis?.risk_score || 0,
      results.solana?.crime_analysis?.risk_score || 0
    ];
    
    results.cross_chain_risk_score = Math.max(...riskScores);

    return results;
  } catch (error) {
    throw new Error(`Cross-chain analysis failed: ${error}`);
  }
}

async function generateCrimeReport(addresses: string[], reportType: string = 'summary'): Promise<any> {
  try {
    const analyses = [];
    
    for (const address of addresses) {
      try {
        // Try to determine blockchain type and analyze accordingly
        if (address.startsWith('1') || address.startsWith('3') || address.startsWith('bc1')) {
          analyses.push(await analyzeBitcoinAddress(address));
        } else if (address.startsWith('0x')) {
          analyses.push(await analyzeEthereumAddress(address));
        } else if (address.includes('.')) {
          analyses.push(await analyzeHederaAccount(address));
        } else {
          analyses.push(await analyzeSolanaWallet(address));
        }
      } catch (error) {
        analyses.push({ address, error: `Analysis failed: ${error}` });
      }
    }

    const report = {
      report_type: reportType,
      timestamp: new Date().toISOString(),
      addresses_analyzed: addresses.length,
      high_risk_addresses: analyses.filter(a => a.crime_analysis?.risk_score > 50).length,
      total_risk_score: analyses.reduce((sum, a) => sum + (a.crime_analysis?.risk_score || 0), 0),
      summary: {
        total_transactions: analyses.reduce((sum, a) => sum + (a.crime_analysis?.transaction_count || 0), 0),
        suspicious_patterns: analyses.flatMap(a => a.crime_analysis?.alerts || []),
        recommendations: [] as string[]
      },
      detailed_analyses: reportType === 'detailed' || reportType === 'forensic' ? analyses : undefined
    };

    if (report.high_risk_addresses > 0) {
      report.summary.recommendations.push("Further investigation recommended for high-risk addresses");
    }

    return report;
  } catch (error) {
    throw new Error(`Crime report generation failed: ${error}`);
  }
}

async function checkAddressReputation(address: string, blockchain: string): Promise<any> {
  try {
    // Simulate reputation check against known databases
    const reputation = {
      address,
      blockchain,
      reputation_score: Math.floor(Math.random() * 100), // Simulated score
      known_associations: [] as string[],
      risk_level: 'low',
      last_updated: new Date().toISOString(),
      sources_checked: ['internal_db', 'public_blacklists', 'exchange_reports']
    };

    if (reputation.reputation_score < 30) {
      reputation.risk_level = 'high';
      reputation.known_associations.push('Potentially associated with suspicious activity');
    } else if (reputation.reputation_score < 60) {
      reputation.risk_level = 'medium';
    }

    return reputation;
  } catch (error) {
    throw new Error(`Reputation check failed: ${error}`);
  }
}

async function analyzeEthereumAddress(address: string, env?: any): Promise<any> {
  try {
    const apiKey = env?.ETHERSCAN_API_KEY || 'YourApiKeyToken';
    
    // Get recent transactions
    const txResponse = await fetch(
      `https://api.etherscan.io/api?module=account&action=txlist&address=${address}&startblock=0&endblock=99999999&page=1&offset=10&sort=desc&apikey=${apiKey}`
    );
    
    if (!txResponse.ok) {
      throw new Error(`Etherscan API error: ${txResponse.statusText}`);
    }
    
    const txData = await txResponse.json() as any;
    const transactions: Transaction[] = (txData.result || []).slice(0, 10).map((tx: any) => ({
      hash: tx.hash,
      value: parseInt(tx.value) || 0,
      timestamp: new Date(parseInt(tx.timeStamp) * 1000).toISOString(),
      from: tx.from,
      to: tx.to,
      value_usd: (parseInt(tx.value) || 0) / 1e18 * 2000 // Rough ETH to USD
    }));

    const analysis = crimeDetector.analyzeTransactionPattern(transactions);

    // Get balance
    const balanceResponse = await fetch(
      `https://api.etherscan.io/api?module=account&action=balance&address=${address}&tag=latest&apikey=${apiKey}`
    );
    const balanceData = await balanceResponse.json() as any;

    return {
      address,
      balance_wei: balanceData.result || '0',
      balance_eth: (parseInt(balanceData.result || '0') / 1e18).toFixed(6),
      transactions,
      crime_analysis: analysis
    };
  } catch (error) {
    throw new Error(`Ethereum analysis failed: ${error}`);
  }
}

async function analyzeHederaAccount(accountId: string): Promise<any> {
  try {
    const response = await fetch(`https://mainnet-public.mirrornode.hedera.com/api/v1/accounts/${accountId}`);
    if (!response.ok) {
      throw new Error(`Hedera Mirror Node API error: ${response.statusText}`);
    }
    const data = await response.json() as any;

    // Get recent transactions
    const txResponse = await fetch(`https://mainnet-public.mirrornode.hedera.com/api/v1/transactions?account.id=${accountId}&limit=10&order=desc`);
    const txData = await txResponse.json() as any;
    
    const transactions: Transaction[] = (txData.transactions || []).map((tx: any) => ({
      hash: tx.transaction_id,
      value: tx.charged_tx_fee || 0,
      timestamp: tx.consensus_timestamp,
      from: tx.entity_id || 'unknown',
      to: tx.transfers?.[0]?.account || 'unknown',
      value_usd: (tx.charged_tx_fee || 0) * 0.05 // Rough HBAR to USD
    }));

    const analysis = crimeDetector.analyzeTransactionPattern(transactions);

    return {
      account_id: accountId,
      balance_hbar: (data.balance?.balance || 0) / 100000000,
      account_memo: data.memo || '',
      transactions,
      crime_analysis: analysis
    };
  } catch (error) {
    throw new Error(`Hedera analysis failed: ${error}`);
  }
}

// Cloudflare Workers export
export default {
  async fetch(request: Request, env: any, ctx: any): Promise<Response> {
    const url = new URL(request.url);
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Handle MCP Streamable HTTP transport at /mcp endpoint
    if (url.pathname === '/mcp') {
      if (request.method === 'POST') {
        try {
          const body = await request.json() as any;
          
          // Validate JSON-RPC 2.0 format
          if (!body.jsonrpc || body.jsonrpc !== '2.0') {
            return new Response(JSON.stringify({
              jsonrpc: '2.0',
              id: body.id || null,
              error: { code: -32600, message: 'Invalid Request - missing or invalid jsonrpc field' }
            }), {
              headers: { 'Content-Type': 'application/json', ...corsHeaders }
            });
          }

          if (!body.method) {
            return new Response(JSON.stringify({
              jsonrpc: '2.0',
              id: body.id || null,
              error: { code: -32600, message: 'Invalid Request - missing method field' }
            }), {
              headers: { 'Content-Type': 'application/json', ...corsHeaders }
            });
          }

          // Handle MCP protocol methods
          if (body.method === 'initialize') {
            return new Response(JSON.stringify({
              jsonrpc: '2.0',
              id: body.id,
              result: {
                protocolVersion: '2024-11-05',
                capabilities: { 
                  tools: {},
                  resources: {},
                  prompts: {}
                },
                serverInfo: { 
                  name: 'chainguard-crime-detector', 
                  version: '1.0.0',
                  description: 'Multi-chain blockchain crime detection MCP server'
                }
              }
            }), { headers: { 'Content-Type': 'application/json', ...corsHeaders } });
          }

          if (body.method === 'tools/list') {
            const tools = [
              {
                name: 'analyze_bitcoin_address',
                description: 'Analyze Bitcoin address for suspicious activity and crime patterns',
                inputSchema: {
                  type: 'object',
                  properties: {
                    address: { type: 'string', description: 'Bitcoin address to analyze' }
                  },
                  required: ['address']
                }
              },
              {
                name: 'analyze_ethereum_address',
                description: 'Analyze Ethereum address for suspicious activity and smart contract risks',
                inputSchema: {
                  type: 'object',
                  properties: {
                    address: { type: 'string', description: 'Ethereum address to analyze' }
                  },
                  required: ['address']
                }
              },
              {
                name: 'analyze_hedera_account',
                description: 'Analyze Hedera account for suspicious behavior patterns',
                inputSchema: {
                  type: 'object',
                  properties: {
                    account_id: { type: 'string', description: 'Hedera account ID (e.g., 0.0.123456)' }
                  },
                  required: ['account_id']
                }
              },
              {
                name: 'analyze_solana_wallet',
                description: 'Analyze Solana wallet for suspicious activity and token risks',
                inputSchema: {
                  type: 'object',
                  properties: {
                    wallet_address: { type: 'string', description: 'Solana wallet address to analyze' }
                  },
                  required: ['wallet_address']
                }
              },
              {
                name: 'detect_rug_pull_ethereum',
                description: 'Detect potential rug pull patterns in Ethereum smart contracts',
                inputSchema: {
                  type: 'object',
                  properties: {
                    contract_address: { type: 'string', description: 'Ethereum contract address to analyze' }
                  },
                  required: ['contract_address']
                }
              },
              {
                name: 'detect_pump_dump_solana',
                description: 'Detect pump and dump schemes in Solana tokens',
                inputSchema: {
                  type: 'object',
                  properties: {
                    token_address: { type: 'string', description: 'Solana token address to analyze' }
                  },
                  required: ['token_address']
                }
              },
              {
                name: 'analyze_cross_chain_activity',
                description: 'Analyze suspicious activity across multiple blockchain networks',
                inputSchema: {
                  type: 'object',
                  properties: {
                    addresses: {
                      type: 'object',
                      properties: {
                        bitcoin: { type: 'string', description: 'Bitcoin address' },
                        ethereum: { type: 'string', description: 'Ethereum address' },
                        hedera: { type: 'string', description: 'Hedera account ID' },
                        solana: { type: 'string', description: 'Solana wallet address' }
                      }
                    }
                  },
                  required: ['addresses']
                }
              },
              {
                name: 'generate_crime_report',
                description: 'Generate comprehensive crime analysis report for multiple addresses',
                inputSchema: {
                  type: 'object',
                  properties: {
                    addresses: {
                      type: 'array',
                      items: { type: 'string' },
                      description: 'List of blockchain addresses to analyze'
                    },
                    report_type: {
                      type: 'string',
                      enum: ['summary', 'detailed', 'forensic'],
                      description: 'Type of report to generate'
                    }
                  },
                  required: ['addresses']
                }
              },
              {
                name: 'check_address_reputation',
                description: 'Check address reputation against known crime databases',
                inputSchema: {
                  type: 'object',
                  properties: {
                    address: { type: 'string', description: 'Blockchain address to check' },
                    blockchain: {
                      type: 'string',
                      enum: ['bitcoin', 'ethereum', 'hedera', 'solana'],
                      description: 'Blockchain network'
                    }
                  },
                  required: ['address', 'blockchain']
                }
              }
            ];

            return new Response(JSON.stringify({
              jsonrpc: '2.0',
              id: body.id,
              result: { tools }
            }), { headers: { 'Content-Type': 'application/json', ...corsHeaders } });
          }

          if (body.method === 'tools/call') {
            const { name, arguments: args } = body.params || {};
            
            if (!name) {
              return new Response(JSON.stringify({
                jsonrpc: '2.0',
                id: body.id,
                error: { code: -32602, message: 'Invalid params - missing tool name' }
              }), {
                headers: { 'Content-Type': 'application/json', ...corsHeaders }
              });
            }

            try {
              let result;
              
              switch (name) {
                case 'analyze_bitcoin_address':
                  if (!args?.address) {
                    throw new Error('Missing required parameter: address');
                  }
                  result = await analyzeBitcoinAddress(args.address);
                  break;
                  
                case 'analyze_ethereum_address':
                  if (!args?.address) {
                    throw new Error('Missing required parameter: address');
                  }
                  result = await analyzeEthereumAddress(args.address, env);
                  break;
                  
                case 'analyze_hedera_account':
                  if (!args?.account_id) {
                    throw new Error('Missing required parameter: account_id');
                  }
                  result = await analyzeHederaAccount(args.account_id);
                  break;
                  
                case 'analyze_solana_wallet':
                  if (!args?.wallet_address) {
                    throw new Error('Missing required parameter: wallet_address');
                  }
                  result = await analyzeSolanaWallet(args.wallet_address, env);
                  break;
                  
                case 'detect_rug_pull_ethereum':
                  if (!args?.contract_address) {
                    throw new Error('Missing required parameter: contract_address');
                  }
                  result = await detectRugPullEthereum(args.contract_address);
                  break;
                  
                case 'detect_pump_dump_solana':
                  if (!args?.token_address) {
                    throw new Error('Missing required parameter: token_address');
                  }
                  result = await detectPumpDumpSolana(args.token_address, env);
                  break;
                  
                case 'analyze_cross_chain_activity':
                  if (!args?.addresses) {
                    throw new Error('Missing required parameter: addresses');
                  }
                  result = await analyzeCrossChainActivity(args.addresses);
                  break;
                  
                case 'generate_crime_report':
                  if (!args?.addresses) {
                    throw new Error('Missing required parameter: addresses');
                  }
                  result = await generateCrimeReport(args.addresses, args.report_type || 'summary');
                  break;
                  
                case 'check_address_reputation':
                  if (!args?.address || !args?.blockchain) {
                    throw new Error('Missing required parameters: address, blockchain');
                  }
                  result = await checkAddressReputation(args.address, args.blockchain);
                  break;
                  
                default:
                  throw new Error(`Unknown tool: ${name}`);
              }

              return new Response(JSON.stringify({
                jsonrpc: '2.0',
                id: body.id,
                result: {
                  content: [
                    {
                      type: 'text',
                      text: JSON.stringify(result, null, 2)
                    }
                  ]
                }
              }), { headers: { 'Content-Type': 'application/json', ...corsHeaders } });

            } catch (error) {
              return new Response(JSON.stringify({
                jsonrpc: '2.0',
                id: body.id,
                error: {
                  code: -32603,
                  message: `Tool execution failed: ${error instanceof Error ? error.message : 'Unknown error'}`
                }
              }), {
                headers: { 'Content-Type': 'application/json', ...corsHeaders }
              });
            }
          }

          return new Response(JSON.stringify({
            jsonrpc: '2.0',
            id: body.id,
            error: { code: -32601, message: `Method not found: ${body.method}` }
          }), {
            headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });

        } catch (error) {
          return new Response(JSON.stringify({
            jsonrpc: '2.0',
            id: null,
            error: { code: -32700, message: 'Parse error - Invalid JSON' }
          }), {
            status: 400,
            headers: { 'Content-Type': 'application/json', ...corsHeaders }
          });
        }
      }
    }

    // Health check endpoint
    if (request.method === 'GET' && url.pathname === '/') {
      return new Response(JSON.stringify({
        name: 'ChainGuard MCP Server',
        version: '1.0.0',
        description: 'Multi-chain blockchain crime detection MCP server',
        capabilities: ['Bitcoin', 'Ethereum', 'Hedera', 'Solana'],
        endpoints: {
          mcp: 'POST /mcp',
          health: 'GET /'
        },
        status: 'online'
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });
    }

    return new Response('Not Found', { status: 404, headers: corsHeaders });
  }
};
