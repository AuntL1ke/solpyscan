import asyncio
from solana_sdk.client import SolanaClient

async def main():
    client = SolanaClient()
    pubkey = "4AwWXsh4R911Ho7qqjmwYdkc7wijmHeYdMyBcVfBaUqZ"

    # Get balance
    balance = await client.get_balance(pubkey)
    print("Balance:", balance, "SOL")

    # Get recent blockhash
    blockhash = await client.get_recent_blockhash()
    print("Blockhash:", blockhash)

    # Get block height
    height = await client.get_block_height()
    print("Block height:", height)

    # Get account info
    account = await client.get_account_info(pubkey)
    print("Account info:", account)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
