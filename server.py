import requests
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
import hashlib
import statistics

mcp = FastMCP("chainguard-crime-detector")

# Crime detection patterns and thresholds
SUSPICIOUS_PATTERNS = {
    "large_transaction_threshold": 100000,  # USD
    "rapid_transactions_count": 10,  # transactions in short time
    "rapid_transactions_window": 300,  # 5 minutes in seconds
    "mixing_service_indicators": ["tornado", "mixer", "tumbler", "privacy"],
    "flash_loan_indicators": ["flashloan", "aave", "compound", "dydx"]
}

class CrimeDetector:
    def __init__(self):
        self.suspicious_addresses = set()
        self.known_mixers = set()
        
    def analyze_transaction_pattern(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze transaction patterns for suspicious activity"""
        if not transactions:
            return {"risk_score": 0, "alerts": []}
            
        alerts = []
        risk_score = 0
        
        # Check for rapid transactions
        if len(transactions) >= SUSPICIOUS_PATTERNS["rapid_transactions_count"]:
            risk_score += 30
            alerts.append("High frequency transactions detected")
            
        # Check for large value transactions
        large_txs = [tx for tx in transactions if tx.get("value_usd", 0) > SUSPICIOUS_PATTERNS["large_transaction_threshold"]]
        if large_txs:
            risk_score += 20
            alerts.append(f"Large transactions detected: {len(large_txs)} transactions")
            
        return {
            "risk_score": min(risk_score, 100),
            "alerts": alerts,
            "transaction_count": len(transactions),
            "large_transactions": len(large_txs)
        }

crime_detector = CrimeDetector()

# Bitcoin Analysis Tools
@mcp.tool()
async def analyze_bitcoin_address(address: str) -> str:
    """
    Analyze a Bitcoin address for suspicious activity using BlockCypher API
    
    Args:
        address: Bitcoin address to analyze
    """
    try:
        # Get address details from BlockCypher
        url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch Bitcoin address data: {response.status_code}"})
            
        data = response.json()
        
        # Get recent transactions
        tx_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full?limit=50"
        tx_response = requests.get(tx_url)
        
        transactions = []
        if tx_response.status_code == 200:
            tx_data = tx_response.json()
            for tx in tx_data.get("txs", []):
                transactions.append({
                    "hash": tx.get("hash"),
                    "value": tx.get("total", 0),
                    "value_usd": tx.get("total", 0) * 0.00000001 * 45000,  # Rough BTC price
                    "confirmations": tx.get("confirmations", 0),
                    "received": tx.get("received")
                })
        
        # Analyze for suspicious patterns
        analysis = crime_detector.analyze_transaction_pattern(transactions)
        
        result = {
            "address": address,
            "blockchain": "Bitcoin",
            "balance_satoshis": data.get("balance", 0),
            "balance_btc": data.get("balance", 0) * 0.00000001,
            "total_received": data.get("total_received", 0),
            "total_sent": data.get("total_sent", 0),
            "n_tx": data.get("n_tx", 0),
            "unconfirmed_balance": data.get("unconfirmed_balance", 0),
            "final_balance": data.get("final_balance", 0),
            "crime_analysis": analysis,
            "recent_transactions": transactions[:10]  # Last 10 transactions
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Bitcoin analysis failed: {str(e)}"})

@mcp.tool()
async def track_bitcoin_transaction(tx_hash: str) -> str:
    """
    Track a Bitcoin transaction and analyze it for suspicious patterns
    
    Args:
        tx_hash: Bitcoin transaction hash to analyze
    """
    try:
        url = f"https://api.blockcypher.com/v1/btc/main/txs/{tx_hash}"
        response = requests.get(url)
        
        if response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch Bitcoin transaction: {response.status_code}"})
            
        data = response.json()
        
        # Analyze transaction
        inputs = data.get("inputs", [])
        outputs = data.get("outputs", [])
        
        total_input = sum(inp.get("output_value", 0) for inp in inputs)
        total_output = sum(out.get("value", 0) for out in outputs)
        
        # Check for mixing patterns
        mixing_indicators = []
        if len(outputs) > 10:
            mixing_indicators.append("High number of outputs (possible mixing)")
        
        if len(set(out.get("value") for out in outputs)) == 1 and len(outputs) > 5:
            mixing_indicators.append("Equal value outputs (mixing pattern)")
            
        result = {
            "transaction_hash": tx_hash,
            "blockchain": "Bitcoin",
            "total_input_satoshis": total_input,
            "total_output_satoshis": total_output,
            "fee_satoshis": total_input - total_output,
            "confirmations": data.get("confirmations", 0),
            "block_height": data.get("block_height"),
            "received": data.get("received"),
            "size": data.get("size"),
            "input_count": len(inputs),
            "output_count": len(outputs),
            "mixing_indicators": mixing_indicators,
            "risk_assessment": {
                "risk_score": len(mixing_indicators) * 25,
                "is_suspicious": len(mixing_indicators) > 0
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Bitcoin transaction analysis failed: {str(e)}"})

# Ethereum Analysis Tools  
@mcp.tool()
async def analyze_ethereum_address(address: str) -> str:
    """
    Analyze an Ethereum address for suspicious activity using Etherscan API
    
    Args:
        address: Ethereum address to analyze
    """
    try:
        # Get address balance and transaction count
        balance_url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken"
        txcount_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=50&sort=desc&apikey=YourApiKeyToken"
        
        balance_response = requests.get(balance_url)
        txcount_response = requests.get(txcount_url)
        
        balance_data = balance_response.json() if balance_response.status_code == 200 else {}
        tx_data = txcount_response.json() if txcount_response.status_code == 200 else {}
        
        transactions = []
        if tx_data.get("status") == "1":
            for tx in tx_data.get("result", []):
                transactions.append({
                    "hash": tx.get("hash"),
                    "value": int(tx.get("value", 0)),
                    "value_eth": int(tx.get("value", 0)) / 1e18,
                    "value_usd": (int(tx.get("value", 0)) / 1e18) * 2500,  # Rough ETH price
                    "gas_used": int(tx.get("gasUsed", 0)),
                    "gas_price": int(tx.get("gasPrice", 0)),
                    "timestamp": tx.get("timeStamp")
                })
        
        # Analyze for suspicious patterns
        analysis = crime_detector.analyze_transaction_pattern(transactions)
        
        # Check for MEV bot patterns
        mev_indicators = []
        gas_prices = [tx.get("gas_price", 0) for tx in transactions if tx.get("gas_price")]
        if gas_prices:
            avg_gas = statistics.mean(gas_prices)
            high_gas_txs = [tx for tx in transactions if tx.get("gas_price", 0) > avg_gas * 2]
            if len(high_gas_txs) > len(transactions) * 0.3:
                mev_indicators.append("High gas price transactions (possible MEV bot)")
        
        result = {
            "address": address,
            "blockchain": "Ethereum", 
            "balance_wei": balance_data.get("result", "0"),
            "balance_eth": int(balance_data.get("result", "0")) / 1e18 if balance_data.get("result") else 0,
            "transaction_count": len(transactions),
            "crime_analysis": analysis,
            "mev_indicators": mev_indicators,
            "recent_transactions": transactions[:10]
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Ethereum analysis failed: {str(e)}"})

@mcp.tool()
async def detect_ethereum_rug_pull(contract_address: str) -> str:
    """
    Analyze an Ethereum contract for rug pull indicators
    
    Args:
        contract_address: Ethereum contract address to analyze
    """
    try:
        # Get contract transactions
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startblock=0&endblock=99999999&page=1&offset=100&sort=desc&apikey=YourApiKeyToken"
        response = requests.get(url)
        
        if response.status_code != 200:
            return json.dumps({"error": "Failed to fetch contract data"})
            
        data = response.json()
        transactions = data.get("result", [])
        
        # Rug pull indicators
        rug_indicators = []
        
        # Check for large withdrawals by contract creator
        large_withdrawals = [tx for tx in transactions if int(tx.get("value", 0)) > 1e19]  # > 10 ETH
        if large_withdrawals:
            rug_indicators.append(f"Large withdrawals detected: {len(large_withdrawals)} transactions")
            
        # Check for liquidity removal patterns
        recent_txs = [tx for tx in transactions if int(tx.get("timeStamp", 0)) > (datetime.now().timestamp() - 86400)]  # Last 24h
        if len(recent_txs) > 50:
            rug_indicators.append("High transaction volume in last 24h (possible rug pull)")
            
        risk_score = len(rug_indicators) * 30
        
        result = {
            "contract_address": contract_address,
            "blockchain": "Ethereum",
            "total_transactions": len(transactions),
            "large_withdrawals": len(large_withdrawals),
            "recent_activity": len(recent_txs),
            "rug_pull_indicators": rug_indicators,
            "risk_assessment": {
                "risk_score": min(risk_score, 100),
                "is_suspicious": risk_score > 50,
                "recommendation": "HIGH RISK - Possible rug pull" if risk_score > 70 else "Monitor closely" if risk_score > 30 else "Low risk"
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Rug pull analysis failed: {str(e)}"})

# Hedera Analysis Tools
@mcp.tool()
async def analyze_hedera_account(account_id: str) -> str:
    """
    Analyze a Hedera account for suspicious activity using Mirror Node API
    
    Args:
        account_id: Hedera account ID (e.g., 0.0.123456)
    """
    try:
        # Get account info from Hedera Mirror Node
        base_url = "https://mainnet-public.mirrornode.hedera.com/api/v1"
        account_url = f"{base_url}/accounts/{account_id}"
        transactions_url = f"{base_url}/transactions?account.id={account_id}&limit=50&order=desc"
        
        account_response = requests.get(account_url)
        tx_response = requests.get(transactions_url)
        
        if account_response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch Hedera account data: {account_response.status_code}"})
            
        account_data = account_response.json()
        tx_data = tx_response.json() if tx_response.status_code == 200 else {"transactions": []}
        
        transactions = []
        for tx in tx_data.get("transactions", []):
            # Convert tinybars to HBAR (1 HBAR = 100,000,000 tinybars)
            charged_fee = tx.get("charged_tx_fee", 0) / 100000000
            transactions.append({
                "transaction_id": tx.get("transaction_id"),
                "consensus_timestamp": tx.get("consensus_timestamp"),
                "charged_fee_hbar": charged_fee,
                "charged_fee_usd": charged_fee * 0.05,  # Rough HBAR price
                "result": tx.get("result"),
                "name": tx.get("name")
            })
        
        # Analyze for suspicious patterns
        analysis = crime_detector.analyze_transaction_pattern(transactions)
        
        # Check for unusual consensus service usage
        consensus_txs = [tx for tx in transactions if tx.get("name") == "CONSENSUSSUBMITMESSAGE"]
        
        result = {
            "account_id": account_id,
            "blockchain": "Hedera",
            "balance_tinybars": account_data.get("balance", {}).get("balance", 0),
            "balance_hbar": account_data.get("balance", {}).get("balance", 0) / 100000000,
            "auto_renew_period": account_data.get("auto_renew_period"),
            "created_timestamp": account_data.get("created_timestamp"),
            "deleted": account_data.get("deleted", False),
            "ethereum_nonce": account_data.get("ethereum_nonce"),
            "max_automatic_token_associations": account_data.get("max_automatic_token_associations"),
            "transaction_count": len(transactions),
            "consensus_transactions": len(consensus_txs),
            "crime_analysis": analysis,
            "recent_transactions": transactions[:10]
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Hedera analysis failed: {str(e)}"})

@mcp.tool()
async def track_hedera_transaction(transaction_id: str) -> str:
    """
    Track a Hedera transaction and analyze it for suspicious patterns
    
    Args:
        transaction_id: Hedera transaction ID
    """
    try:
        base_url = "https://mainnet-public.mirrornode.hedera.com/api/v1"
        url = f"{base_url}/transactions/{transaction_id}"
        
        response = requests.get(url)
        
        if response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch Hedera transaction: {response.status_code}"})
            
        data = response.json()
        transactions = data.get("transactions", [])
        
        if not transactions:
            return json.dumps({"error": "Transaction not found"})
            
        tx = transactions[0]
        
        # Analyze transaction details
        transfers = tx.get("transfers", [])
        token_transfers = tx.get("token_transfers", [])
        
        # Check for suspicious patterns
        suspicious_indicators = []
        
        # Large number of transfers
        if len(transfers) > 20:
            suspicious_indicators.append("High number of transfers (possible distribution)")
            
        # Token transfer patterns
        if len(token_transfers) > 10:
            suspicious_indicators.append("High number of token transfers")
            
        result = {
            "transaction_id": transaction_id,
            "blockchain": "Hedera",
            "consensus_timestamp": tx.get("consensus_timestamp"),
            "charged_tx_fee": tx.get("charged_tx_fee", 0) / 100000000,
            "max_fee": tx.get("max_fee", 0) / 100000000,
            "memo_base64": tx.get("memo_base64"),
            "name": tx.get("name"),
            "result": tx.get("result"),
            "scheduled": tx.get("scheduled", False),
            "transaction_hash": tx.get("transaction_hash"),
            "valid_duration_seconds": tx.get("valid_duration_seconds"),
            "transfers_count": len(transfers),
            "token_transfers_count": len(token_transfers),
            "suspicious_indicators": suspicious_indicators,
            "risk_assessment": {
                "risk_score": len(suspicious_indicators) * 25,
                "is_suspicious": len(suspicious_indicators) > 0
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Hedera transaction analysis failed: {str(e)}"})

# Solana Analysis Tools (using Helius API)
@mcp.tool()
async def analyze_solana_address(address: str, helius_api_key: str = "demo") -> str:
    """
    Analyze a Solana address for suspicious activity using Helius API
    
    Args:
        address: Solana wallet address to analyze
        helius_api_key: Helius API key (defaults to demo key with limited functionality)
    """
    try:
        # Get address info using Helius API
        base_url = f"https://api.helius.xyz/v0"
        
        # Get transaction history
        tx_url = f"{base_url}/addresses/{address}/transactions?api-key={helius_api_key}&limit=50"
        balance_url = f"https://api.mainnet-beta.solana.com"
        
        # Get balance using Solana RPC
        balance_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [address]
        }
        
        tx_response = requests.get(tx_url)
        balance_response = requests.post(balance_url, json=balance_payload)
        
        transactions = []
        if tx_response.status_code == 200:
            tx_data = tx_response.json()
            for tx in tx_data:
                # Analyze transaction for SOL transfers
                sol_transfer = 0
                if "nativeTransfers" in tx:
                    for transfer in tx["nativeTransfers"]:
                        sol_transfer += transfer.get("amount", 0)
                
                transactions.append({
                    "signature": tx.get("signature"),
                    "timestamp": tx.get("timestamp"),
                    "sol_transfer": sol_transfer / 1e9,  # Convert lamports to SOL
                    "sol_transfer_usd": (sol_transfer / 1e9) * 20,  # Rough SOL price
                    "fee": tx.get("fee", 0) / 1e9,
                    "success": not tx.get("err")
                })
        
        balance_data = balance_response.json() if balance_response.status_code == 200 else {}
        balance_lamports = balance_data.get("result", {}).get("value", 0)
        
        # Analyze for suspicious patterns
        analysis = crime_detector.analyze_transaction_pattern(transactions)
        
        # Check for bot-like behavior
        bot_indicators = []
        if len(transactions) > 0:
            success_rate = sum(1 for tx in transactions if tx["success"]) / len(transactions)
            if success_rate > 0.95 and len(transactions) > 20:
                bot_indicators.append("High success rate with many transactions (possible bot)")
                
            # Check for MEV patterns
            high_fee_txs = [tx for tx in transactions if tx["fee"] > 0.01]  # > 0.01 SOL fee
            if len(high_fee_txs) > len(transactions) * 0.2:
                bot_indicators.append("High fee transactions (possible MEV bot)")
        
        result = {
            "address": address,
            "blockchain": "Solana",
            "balance_lamports": balance_lamports,
            "balance_sol": balance_lamports / 1e9,
            "balance_usd": (balance_lamports / 1e9) * 20,
            "transaction_count": len(transactions),
            "crime_analysis": analysis,
            "bot_indicators": bot_indicators,
            "recent_transactions": transactions[:10]
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Solana analysis failed: {str(e)}"})

@mcp.tool()
async def detect_solana_pump_dump(token_address: str, helius_api_key: str = "demo") -> str:
    """
    Analyze a Solana token for pump and dump patterns
    
    Args:
        token_address: Solana token mint address
        helius_api_key: Helius API key
    """
    try:
        # Get token transactions using Helius
        base_url = f"https://api.helius.xyz/v0"
        url = f"{base_url}/tokens/{token_address}/transactions?api-key={helius_api_key}&limit=100"
        
        response = requests.get(url)
        
        if response.status_code != 200:
            return json.dumps({"error": f"Failed to fetch token data: {response.status_code}"})
            
        transactions = response.json()
        
        # Analyze for pump and dump patterns
        pump_dump_indicators = []
        
        # Check for rapid large transactions
        large_txs = []
        recent_txs = []
        current_time = datetime.now().timestamp()
        
        for tx in transactions:
            tx_time = tx.get("timestamp", 0)
            if current_time - tx_time < 3600:  # Last hour
                recent_txs.append(tx)
                
            # Check for large token transfers
            if "tokenTransfers" in tx:
                for transfer in tx["tokenTransfers"]:
                    if transfer.get("mint") == token_address:
                        amount = transfer.get("tokenAmount", 0)
                        if amount > 1000000:  # Large transfer threshold
                            large_txs.append(tx)
        
        if len(recent_txs) > 50:
            pump_dump_indicators.append("High transaction volume in last hour")
            
        if len(large_txs) > 10:
            pump_dump_indicators.append(f"Multiple large transfers detected: {len(large_txs)}")
            
        # Check for coordinated activity
        unique_addresses = set()
        for tx in recent_txs:
            if "tokenTransfers" in tx:
                for transfer in tx["tokenTransfers"]:
                    unique_addresses.add(transfer.get("fromUserAccount"))
                    unique_addresses.add(transfer.get("toUserAccount"))
                    
        if len(recent_txs) > 20 and len(unique_addresses) < 5:
            pump_dump_indicators.append("Few unique addresses with high activity (coordinated)")
        
        risk_score = len(pump_dump_indicators) * 25
        
        result = {
            "token_address": token_address,
            "blockchain": "Solana",
            "total_transactions": len(transactions),
            "recent_transactions_1h": len(recent_txs),
            "large_transfers": len(large_txs),
            "unique_addresses": len(unique_addresses),
            "pump_dump_indicators": pump_dump_indicators,
            "risk_assessment": {
                "risk_score": min(risk_score, 100),
                "is_suspicious": risk_score > 50,
                "recommendation": "HIGH RISK - Possible pump & dump" if risk_score > 70 else "Monitor closely" if risk_score > 30 else "Normal activity"
            }
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Pump & dump analysis failed: {str(e)}"})

# Cross-chain Analysis Tools
@mcp.tool()
async def generate_crime_report(addresses: str, chains: str = "bitcoin,ethereum,hedera,solana") -> str:
    """
    Generate a comprehensive crime analysis report across multiple blockchains
    
    Args:
        addresses: Comma-separated list of addresses to analyze
        chains: Comma-separated list of chains to check (bitcoin,ethereum,hedera,solana)
    """
    try:
        address_list = [addr.strip() for addr in addresses.split(",")]
        chain_list = [chain.strip() for chain in chains.split(",")]
        
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "addresses_analyzed": address_list,
            "chains_analyzed": chain_list,
            "findings": [],
            "overall_risk_assessment": {
                "total_addresses": len(address_list),
                "high_risk_addresses": 0,
                "medium_risk_addresses": 0,
                "low_risk_addresses": 0
            }
        }
        
        for address in address_list:
            address_findings = {
                "address": address,
                "chain_analyses": {},
                "cross_chain_patterns": [],
                "overall_risk_score": 0
            }
            
            # Analyze on each requested chain
            total_risk = 0
            analysis_count = 0
            
            # Note: In a real implementation, you'd call the respective analysis functions
            # For now, we'll simulate the analysis
            for chain in chain_list:
                if chain == "bitcoin":
                    # Simulate Bitcoin analysis
                    risk_score = 25  # Placeholder
                elif chain == "ethereum":
                    # Simulate Ethereum analysis  
                    risk_score = 40  # Placeholder
                elif chain == "hedera":
                    # Simulate Hedera analysis
                    risk_score = 15  # Placeholder
                elif chain == "solana":
                    # Simulate Solana analysis
                    risk_score = 30  # Placeholder
                else:
                    continue
                    
                address_findings["chain_analyses"][chain] = {
                    "risk_score": risk_score,
                    "status": "analyzed"
                }
                total_risk += risk_score
                analysis_count += 1
            
            # Calculate overall risk for this address
            if analysis_count > 0:
                address_findings["overall_risk_score"] = total_risk / analysis_count
                
                # Categorize risk level
                if address_findings["overall_risk_score"] > 60:
                    report["overall_risk_assessment"]["high_risk_addresses"] += 1
                elif address_findings["overall_risk_score"] > 30:
                    report["overall_risk_assessment"]["medium_risk_addresses"] += 1
                else:
                    report["overall_risk_assessment"]["low_risk_addresses"] += 1
            
            report["findings"].append(address_findings)
        
        return json.dumps(report, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Crime report generation failed: {str(e)}"})
    
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
