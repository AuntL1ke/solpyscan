# solana_sdk/wallet.py

import base58
import binascii
import base64
import asyncio
import json
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solana.rpc.async_api import AsyncClient
from solana.exceptions import SolanaRpcException

DEVNET_RPC = "https://api.devnet.solana.com"

class WalletManager:
    def __init__(self, rpc_url: str = DEVNET_RPC):
        self.client = AsyncClient(rpc_url)

    def create_keypair(self) -> dict:
        kp = Keypair()
        return {
            "public_key": str(kp.pubkey()),
            "private_key": list(kp.to_bytes()),
        }

    def restore_keypair_from_secret(self, secret: list[int]) -> Keypair:
        return Keypair.from_bytes(bytes(secret))

    async def get_balance(self, pubkey: str) -> float:
        pub = Pubkey.from_string(pubkey)
        result = await self.client.get_balance(pub)
        lamports = result.value
        return lamports / 1_000_000_000

    async def request_airdrop(self, pubkey: str, sol: float = 1.0) -> str | None:
        pub = Pubkey.from_string(pubkey)
        lamports = int(sol * 1_000_000_000)
        try:
            resp = await self.client.request_airdrop(pub, lamports)
            return str(resp.value)
        except Exception as e:
            print(f"Airdrop failed automatically: {e}")
            print(f"Please perform a manual airdrop for {pubkey} using https://faucet.solana.com")
            return None

    def sign_message(self, message: str, secret: list[int]) -> str:
        kp = self.restore_keypair_from_secret(secret)
        signature = kp.sign_message(message.encode("utf-8"))
        return base64.b64encode(signature.to_bytes()).decode()

    def verify_keypair(self, secret: list[int], pubkey: str) -> bool:
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

    @staticmethod
    def get_pubkey_from_secret(secret: list[int]) -> str:
        kp = Keypair.from_bytes(bytes(secret))
        return str(kp.pubkey())

    @staticmethod
    def load_wallet_dict(path: str = "wallet.json") -> dict:
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def save_wallet_to_file(wallet: dict, path: str = "wallet.json"):
        with open(path, "w") as f:
            json.dump(wallet, f, indent=4)

    @staticmethod
    def load_wallet_from_file(path: str = "wallet.json") -> Keypair:
        with open(path, "r") as f:
            wallet = json.load(f)
            secret = wallet.get("private_key")
            if not secret:
                raise ValueError("File does not contain the 'private_key' field")
        return Keypair.from_bytes(bytes(secret))

    @staticmethod
    def private_key_to_bytes(secret: list[int]) -> bytes:
        return bytes(secret)

    @staticmethod
    def private_key_to_base64(secret: list[int]) -> str:
        return base64.b64encode(bytes(secret)).decode()

    @staticmethod
    def private_key_to_base58(secret: list[int]) -> str:
        return base58.b58encode(bytes(secret)).decode()

    @staticmethod
    def private_key_to_hex(secret: list[int]) -> str:
        return binascii.hexlify(bytes(secret)).decode()

    @staticmethod
    def private_key_from_base64(encoded: str) -> list[int]:
        return list(base64.b64decode(encoded))

    @staticmethod
    def private_key_from_base58(encoded: str) -> list[int]:
        return list(base58.b58decode(encoded))

    @staticmethod
    def private_key_from_hex(encoded: str) -> list[int]:
        return list(binascii.unhexlify(encoded))

    @staticmethod
    def save_private_key_base64(secret: list[int], path: str = "private_base64.txt"):
        with open(path, "w") as f:
            f.write(WalletManager.private_key_to_base64(secret))

    @staticmethod
    def save_private_key_base58(secret: list[int], path: str = "private_base58.txt"):
        with open(path, "w") as f:
            f.write(WalletManager.private_key_to_base58(secret))

    @staticmethod
    def save_private_key_hex(secret: list[int], path: str = "private_hex.txt"):
        with open(path, "w") as f:
            f.write(WalletManager.private_key_to_hex(secret))

    @staticmethod
    def load_private_key_from_base64_file(path: str) -> list[int]:
        with open(path, "r") as f:
            return WalletManager.private_key_from_base64(f.read().strip())

    @staticmethod
    def load_private_key_from_base58_file(path: str) -> list[int]:
        with open(path, "r") as f:
            return WalletManager.private_key_from_base58(f.read().strip())

    @staticmethod
    def load_private_key_from_hex_file(path: str) -> list[int]:
        with open(path, "r") as f:
            return WalletManager.private_key_from_hex(f.read().strip())

    
    async def close(self):
        await self.client.close()
