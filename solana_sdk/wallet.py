from .client import SolanaClient

class WalletAnalyzer:
    def __init__(self, client: SolanaClient):
        self.client = client

    def get_balance(self, address: str) -> float:
        res = self.client.get_balance(address)
        lamports = res.value  
        return lamports / 1_000_000_000
