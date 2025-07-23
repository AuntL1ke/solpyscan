# solana_sdk/wallet.py

import base64
import asyncio
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solana.rpc.async_api import AsyncClient
from solana.exceptions import SolanaRpcException

#  можливість міняти RPC провайдери
DEVNET_RPC = "https://api.devnet.solana.com"

class WalletManager:
    def __init__(self, rpc_url: str = DEVNET_RPC):
        self.client = AsyncClient(rpc_url)

    # Це не сід фраза а приватний ключ треба буде поміянти і додати створення сід фрази
    def create_keypair(self) -> dict:
        kp = Keypair()
        return {
            "public_key": str(kp.pubkey()),
            "private_key": list(kp.to_bytes()),
        }

    def restore_keypair_from_secret(self, secret: list) -> Keypair:
        return Keypair.from_bytes(bytes(secret))

    async def get_balance(self, pubkey: str) -> float:
        pub = Pubkey.from_string(pubkey)
        result = await self.client.get_balance(pub)
        lamports = result.value
        return lamports / 1_000_000_000

    async def request_airdrop(self, pubkey: str, sol: float = 1.0, retries: int = 3) -> str | None:
        pub = Pubkey.from_string(pubkey)
        lamports = int(sol * 1_000_000_000)

        for attempt in range(1, retries + 1):
            try:
                resp = await self.client.request_airdrop(pub, lamports)
                return str(resp.value)
            except SolanaRpcException as e:
                print(f"Airdrop failed (attempt {attempt}/{retries}): {str(e) or type(e).__name__}")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Unknown error during airdrop: {e}")
                break

        print("Airdrop failed after multiple attempts. Continuing without SOL.")
        return None

    def sign_message(self, message: str, secret: list) -> str:
        kp = self.restore_keypair_from_secret(secret)
        signature = kp.sign_message(message.encode("utf-8"))
        return base64.b64encode(signature.to_bytes()).decode()

    def verify_keypair(self, secret: list, pubkey: str) -> bool:
        try:
            kp = self.restore_keypair_from_secret(secret)
            return str(kp.pubkey()) == pubkey
        except:
            return False

    def validate_pubkey(self, pubkey: str) -> bool:
        try:
            _ = Pubkey.from_string(pubkey)
            return True
        except:
            return False

    async def close(self):
        await self.client.close()
