from solana.rpc.api import Client
from solders.pubkey import Pubkey  

class SolanaClient:
    def __init__(self, endpoint="https://api.mainnet-beta.solana.com"):
        self.client = Client(endpoint)

    def get_balance(self, pubkey: str):
        pubkey = Pubkey.from_string(pubkey)  
        return self.client.get_balance(pubkey)
