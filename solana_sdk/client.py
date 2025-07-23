from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from typing import Any

class SolanaClient:
    def __init__(self, endpoint: str = "https://api.devnet.solana.com"):
        self.client = AsyncClient(endpoint)

    async def get_balance(self, pubkey: str) -> float:
        pub = Pubkey.from_string(pubkey)
        resp = await self.client.get_balance(pub)
        lamports = resp.value
        return lamports / 1_000_000_000

    async def get_block_height(self) -> int:
        resp = await self.client.get_block_height()
        return resp.value

    async def get_recent_blockhash(self) -> str:
        resp = await self.client.get_latest_blockhash()
        return str(resp.value.blockhash)

    async def get_account_info(self, pubkey: str) -> dict[str, Any] | None:
        pub = Pubkey.from_string(pubkey)
        resp = await self.client.get_account_info(pub)
        return resp.value

    async def close(self):
        await self.client.close()
