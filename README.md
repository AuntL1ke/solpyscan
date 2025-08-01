# SolPyScan SDK

SolPyScan is a Python SDK for interacting with the Solana blockchain. It provides tools for managing wallets, sending transactions, and querying blockchain data. The SDK can be used as a library or as a command-line tool.

## Features
- Wallet management (create, restore, and save wallets).
- Send and receive SOL tokens.
- Query account balances and blockchain data.
- Simple and intuitive API for developers.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

### As a Library

#### Example: Querying Account Balance

```python
import asyncio
from solana_sdk.client import SolanaClient

async def main():
    client = SolanaClient()
    pubkey = "YourPublicKeyHere"

    balance = await client.get_balance(pubkey)
    print(f"Balance: {balance} SOL")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

#### Example: Sending SOL

```python
import asyncio
from solana_sdk.transaction import send_sol

async def main():
    client = SolanaClient()
    sender_secret = [YourSenderSecretKey]
    recipient_pubkey = "RecipientPublicKeyHere"

    tx_signature = await send_sol(client, sender_secret, recipient_pubkey, 0.01)
    print(f"Transaction Signature: {tx_signature}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### As a Command-Line Tool

Run the CLI tool to check wallet balance:

```bash
python cli/main.py --balance YourPublicKeyHere
```

## Examples

Check the `examples/` directory for more usage examples:
- `client_example.py`: Query blockchain data.
- `transaction_example.py`: Send transactions.
- `wallet_example.py`: Manage wallets.

## Testing

To run tests, use:

```bash
pytest tests/
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Roadmap

This project will be developed in 4 main stages:

### ✅ Stage 1: MVP SDK (Completed)
- Wallet management
- Sending SOL
- Adding memos
- Fee estimation
- Transaction analysis

### 🔜 Stage 2: Token SDK
- SPL token minting and transfer
- Associated token accounts (ATA)
- Rent exemption calculation
- Token metadata support

### 🔜 Stage 3: Smart Tools & Analytics
- Real-time account monitoring
- Transaction watchers
- Auto airdrop, alert on balance change
- Transaction history and filters

### 🔜 Stage 4: CLI Tool & Integrations
- Full command-line interface (`solpyscan ...`)
- Telegram bot support
- Jupyter / GPT-powered features

## Why SolPyScan?

SolPyScan is designed for Python developers who want to interact with the Solana blockchain without learning Rust or low-level RPCs. It enables:
- Easy integration into Python apps and scripts
- Devnet prototyping and educational use cases
- Building wallets, tools, and bots in pure Python

## Project Status

✅ Stage 1 completed (MVP SDK released)  
🔜 Stage 2 in development (SPL tokens, accounts)  
⭐ Star this repo to follow updates and contribute!

## Updated CLI Example

Run the CLI tool to check wallet balance:

```bash
python cli/main.py --balance Gs9x123abc...
```
