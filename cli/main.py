import argparse
from solana_sdk.client import SolanaClient
from solana_sdk.wallet import WalletAnalyzer

def main():
    parser = argparse.ArgumentParser(description="Solana CLI Tool")
    parser.add_argument("--balance", help="Check SOL balance for a wallet")
    args = parser.parse_args()

    client = SolanaClient()
    wallet = WalletAnalyzer(client)

    if args.balance:
        sol = wallet.get_balance(args.balance)
        print(f"Balance: {sol} SOL")

if __name__ == "__main__":
    main()
