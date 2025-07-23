import asyncio
from solana_sdk.client import SolanaClient

async def main():
    client = SolanaClient()
    pubkey = "4AwWXsh4R911Ho7qqjmwYdkc7wijmHeYdMyBcVfBaUqZ"

    balance = await client.get_balance(pubkey)
    print("Баланс:", balance, "SOL")

    blockhash = await client.get_recent_blockhash()
    print("Blockhash:", blockhash)

    height = await client.get_block_height()
    print("Block height:", height)

    account = await client.get_account_info(pubkey)
    print("Account info:", account)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
