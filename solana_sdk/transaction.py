from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TxOpts
from solders.system_program import transfer, TransferParams
from solders.signature import Signature
import json

async def send_sol(client: AsyncClient, sender_secret: list, recipient_pubkey: str, amount_sol: float) -> str:
    sender = Keypair.from_bytes(bytes(sender_secret))
    recipient = Pubkey.from_string(recipient_pubkey)
    lamports = int(amount_sol * 1_000_000_000)

    ix: Instruction = transfer(TransferParams(
        from_pubkey=sender.pubkey(),
        to_pubkey=recipient,
        lamports=lamports
    ))

    bh_resp = await client.get_latest_blockhash()
    blockhash = bh_resp.value.blockhash

    msg = MessageV0.try_compile(
        payer=sender.pubkey(),
        instructions=[ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash
    )

    tx = VersionedTransaction(msg, [sender])

    try:
        ʼ
        send_resp = await client.send_transaction(tx, opts=TxOpts(skip_preflight=True))
        await client.confirm_transaction(send_resp.value)
        return str(send_resp.value)
    except Exception as e:
        print("❌ Помилка при переказі:", e)
        return None

async def get_transaction_info(client: AsyncClient, signature_str: str) -> dict | None:
    try:
        signature = Signature.from_string(signature_str)
        resp = await client.get_transaction(
            signature,
            encoding="jsonParsed",
            max_supported_transaction_version=0
        )

        if not resp.value:
            print("❌ Транзакція не знайдена")
            return None

        tx = json.loads(resp.value.to_json())  # <- перетворюємо у звичайний словник

        status = "Невідомо"
        amount = None
        sender = None
        recipient = None

        meta = tx.get("meta", {})
        if meta:
            status = "✅ Успішна" if meta.get("err") is None else f"❌ Помилка: {meta.get('err')}"

        message = tx.get("transaction", {}).get("message", {})
        instructions = message.get("instructions", [])

        for inst in instructions:
            if inst.get("parsed", {}).get("type") == "transfer":
                info = inst["parsed"]["info"]
                sender = info.get("source")
                recipient = info.get("destination")
                amount = int(info.get("lamports", 0)) / 1_000_000_000

        return {
            "Статус": status,
            "Час блоку (Unix)": tx.get("blockTime"),
            "Відправник": sender,
            "Одержувач": recipient,
            "Сума (SOL)": amount,
        }

    except Exception as e:
        print(f"❌ Помилка при отриманні інформації про транзакцію: {e}")
        return None
