import asyncio
import json
from solana_sdk.wallet import WalletManager
from solana_sdk.transaction import TransactionManager
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solders.system_program import transfer, TransferParams

def load_wallet(path="my_wallet.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)

async def main():
    wm = WalletManager()
    tm = TransactionManager(wm.client)

    # Load sender wallet
    sender_wallet = load_wallet()
    sender_secret = sender_wallet['private_key']
    sender_pubkey = sender_wallet['public_key']
    sender_keypair = Keypair.from_bytes(bytes(sender_secret))
    print(f"Sender: {sender_pubkey}")

    # Create a new recipient
    recipient_wallet = wm.create_keypair()
    recipient_pubkey = recipient_wallet['public_key']
    print(f"Recipient: {recipient_pubkey}")

    # Fund recipient
    print("\nFunding recipient with 0.003 SOL...")
    await tm.send_sol(sender_secret, recipient_pubkey, 0.003)

    # Add memo to transaction
    print("\nAdding memo to transaction...")
    memo = "Demo memo"
    ix = transfer(TransferParams(
        from_pubkey=Pubkey.from_string(sender_pubkey),
        to_pubkey=Pubkey.from_string(recipient_pubkey),
        lamports=10_000
    ))
    blockhash = (await wm.client.get_latest_blockhash()).value.blockhash
    msg = MessageV0.try_compile(
        payer=Pubkey.from_string(sender_pubkey),
        instructions=[ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash,
    )
    tx = VersionedTransaction(msg, [sender_keypair])
    await tm.add_memo(tx, memo, Pubkey.from_string(sender_pubkey))

    # Estimate fee
    print("\nEstimating fee...")
    fee = await tm.estimate_fee(tx)
    print("Estimated fee:", fee, "lamports")

    # Sign and send transaction
    print("\nSigning and sending transaction...")
    tx_sig = await tm.sign_and_send_transaction(tx)
    print("Transaction Signature:", tx_sig)

    # Get transaction info
    print("\nGetting transaction info...")
    tx_info = await tm.get_transaction_info(tx_sig)
    print("Transaction Info:", tx_info)

    await wm.close()

if __name__ == "__main__":
    asyncio.run(main())
