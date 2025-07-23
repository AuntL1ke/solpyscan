import asyncio

def main():
    parser = argparse.ArgumentParser(description="Solana CLI Tool")
    parser.add_argument("--balance", help="Check SOL balance for a wallet")
    args = parser.parse_args()

    asyncio.run(run(args))

async def run(args):
    client = SolanaClient()
    wallet = WalletAnalyzer(client)

    if args.balance:
        sol = await wallet.get_balance(args.balance)
        print(f"Balance: {sol / 1_000_000_000:.4f} SOL")

if __name__ == "__main__":
    main()
