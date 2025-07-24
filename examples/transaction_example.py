import asyncio
import json
from solana_sdk.wallet import WalletManager
from solana_sdk.transaction import send_sol, get_transaction_info  # підключено одразу і get_transaction_info

def load_wallet(path="my_wallet.json") -> dict:
    with open(path, "r") as f:
        return json.load(f)

async def main():
    wm = WalletManager()

    # ✅ Завантажуємо відправника з файлу
    sender_wallet = load_wallet()
    sender_secret = sender_wallet['private_key']
    sender_pubkey = sender_wallet['public_key']

    # 🎯 Генеруємо нового отримувача
    recipient_wallet = wm.create_keypair()
    recipient_pubkey = recipient_wallet['public_key']

    print(f"🔑 Sender: {sender_pubkey}")
    print(f"🎯 Recipient: {recipient_pubkey}")

    print("\n💰 Баланс до:")
    print("   Sender:", await wm.get_balance(sender_pubkey), "SOL")
    print("   Recipient:", await wm.get_balance(recipient_pubkey), "SOL")

    # ======= РЕАЛЬНА ТРАНЗАКЦІЯ (закоментована) =======
    # print("\n💸 Відправляємо 0.5 SOL...")
    # tx_sig = await send_sol(wm.client, sender_secret, recipient_pubkey, 0.5)
    # print("📄 Транзакція:", tx_sig)

    # await asyncio.sleep(2)

    print("\n✅ Баланс після:")
    print("   Sender:", await wm.get_balance(sender_pubkey), "SOL")
    print("   Recipient:", await wm.get_balance(recipient_pubkey), "SOL")

    # ======= Перевірка транзакції за підписом (можна вставити вручну) =======
    example_sig = "5wkgsBSZB4E39DkostWys82ZKCa2BY87hxjLBUQM5UfnrCmZcyDz95DtwSTLRpPrcd7DRubjkKVxdULMDVViEQCz"
    tx_info = await get_transaction_info(wm.client, example_sig)
    print("\nℹ️ Інформація про транзакцію:")
    if tx_info:
        for k, v in tx_info.items():
            print(f"{k}: {v}")

    await wm.close()

if __name__ == "__main__":
    asyncio.run(main())
