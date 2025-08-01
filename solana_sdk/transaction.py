from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction, AccountMeta
from solders.transaction import VersionedTransaction
from solders.message import MessageV0, to_bytes_versioned
from solders.system_program import transfer, TransferParams
from solders.signature import Signature
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts

import json


class TransactionManager:
    def __init__(self, client: AsyncClient):
        self.client = client

    async def send_sol(self, sender_secret: list, recipient_pubkey: str, amount_sol: float) -> str:
        sender = Keypair.from_bytes(bytes(sender_secret))
        recipient = Pubkey.from_string(recipient_pubkey)
        lamports = int(amount_sol * 1_000_000_000)

        ix = transfer(TransferParams(
            from_pubkey=sender.pubkey(),
            to_pubkey=recipient,
            lamports=lamports
        ))

        blockhash = (await self.client.get_latest_blockhash()).value.blockhash

        msg = MessageV0.try_compile(
            payer=sender.pubkey(),
            instructions=[ix],
            address_lookup_table_accounts=[],
            recent_blockhash=blockhash
        )

        tx = VersionedTransaction(msg, [sender])

        try:
            send_resp = await self.client.send_transaction(tx, opts=TxOpts(skip_preflight=True))
            await self.client.confirm_transaction(send_resp.value)
            return str(send_resp.value)
        except Exception as e:
            print("Error during transfer:", e)
            return None

    async def add_memo(self, transaction: VersionedTransaction, memo: str, signer_pubkey: Pubkey) -> None:
        memo_ix = Instruction(
            program_id=Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"),
            accounts=[AccountMeta(pubkey=signer_pubkey, is_signer=True, is_writable=False)],
            data=memo.encode("utf-8"),
        )
        transaction.message.instructions.append(memo_ix)

    async def estimate_fee(self, transaction: VersionedTransaction) -> int:
        try:
            fee_resp = await self.client.get_fee_for_message(transaction.message)  # ✅ fixed
            return fee_resp.value
        except Exception as e:
            print(f"Error estimating fee: {e}")
            return 0

    async def sign_and_send_transaction(self, transaction: VersionedTransaction) -> str:
        try:
            raw_tx = bytes(transaction)  # ✅ fixed
            response = await self.client.send_raw_transaction(raw_tx, opts=TxOpts(skip_preflight=True))
            await self.client.confirm_transaction(response.value)
            return str(response.value)
        except Exception as e:
            print(f"Error signing and sending transaction: {e}")
            return None

    async def get_transaction_info(self, signature_str: str) -> dict | None:
        try:
            signature = Signature.from_string(signature_str)
            resp = await self.client.get_transaction(signature, encoding="jsonParsed", max_supported_transaction_version=0)

            if not resp.value:
                print("Transaction not found")
                return None

            tx = json.loads(resp.value.to_json())

            status = "Unknown"
            amount = None
            sender = None
            recipient = None

            meta = tx.get("meta", {})
            if meta:
                status = "Successful" if meta.get("err") is None else f"Error: {meta.get('err')}"

            message = tx.get("transaction", {}).get("message", {})
            instructions = message.get("instructions", [])

            for inst in instructions:
                if inst.get("parsed", {}).get("type") == "transfer":
                    info = inst["parsed"]["info"]
                    sender = info.get("source")
                    recipient = info.get("destination")
                    amount = int(info.get("lamports", 0)) / 1_000_000_000

            return {
                "Status": status,
                "Block Time (Unix)": tx.get("blockTime"),
                "Sender": sender,
                "Recipient": recipient,
                "Amount (SOL)": amount,
            }

        except Exception as e:
            print(f"Error retrieving transaction information: {e}")
            return None
