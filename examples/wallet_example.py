# examples/wallet_example.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from solana_sdk.wallet import WalletManager

async def main():
    wm = WalletManager()

    # Create a new wallet
    wallet = wm.create_keypair()
    pubkey = wallet["public_key"]
    secret = wallet["private_key"]
    print("New Wallet:", wallet)

    # Save wallet to file
    wm.save_wallet_to_file(wallet, "my_wallet.json")
    print("Wallet saved to my_wallet.json")

    # Load wallet from file
    loaded_wallet = wm.load_wallet_from_file("my_wallet.json")
    print("Loaded Wallet Public Key:", loaded_wallet.pubkey())

    # Request airdrop
    print("Requesting airdrop...")
    airdrop_sig = await wm.request_airdrop(pubkey, 1.0)
    print("Airdrop Signature:", airdrop_sig)

    # Get balance
    balance = await wm.get_balance(pubkey)
    print("Wallet Balance:", balance, "SOL")

    # Validate public key
    is_valid = wm.validate_pubkey(pubkey)
    print("Is Public Key Valid:", is_valid)

    await wm.close()

if __name__ == "__main__":
    asyncio.run(main())
