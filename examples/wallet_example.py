# examples/wallet_example.py

import asyncio
import json
from solana_sdk.wallet import WalletManager

async def main():
    wm = WalletManager()

    # 🆕 Створення нового гаманця
    wallet = wm.create_keypair()
    pubkey = wallet["public_key"]
    secret = wallet["private_key"]

    # 💾 Збереження у файл
    wm.save_wallet_to_file(wallet, "my_wallet.json")
    print("💾 Збережено гаманець у my_wallet.json")

    # 🔍 Перевірка валідності
    print("✅ Публічний ключ валідний:", wm.validate_pubkey(pubkey))
    print("✅ Приватний ключ співпадає:", wm.verify_keypair(secret, pubkey))

    # 📂 Завантаження з файлу у Keypair
    kp = wm.load_wallet_from_file("my_wallet.json")
    print("📂 Відновлений публічний ключ:", kp.pubkey())

    # 🔐 Формати приватного ключа
    print("🔐 base64:", wm.private_key_to_base64(secret))
    print("🔐 base58:", wm.private_key_to_base58(secret))
    print("🔐 hex   :", wm.private_key_to_hex(secret))

    # 🔁 Відновлення з кожного формату
    restored_b64 = wm.private_key_from_base64(wm.private_key_to_base64(secret))
    restored_b58 = wm.private_key_from_base58(wm.private_key_to_base58(secret))
    restored_hex = wm.private_key_from_hex(wm.private_key_to_hex(secret))

    print("✅ Base64 відновлено:", restored_b64 == secret)
    print("✅ Base58 відновлено:", restored_b58 == secret)
    print("✅ Hex відновлено   :", restored_hex == secret)

    # 🧾 Баланс (Devnet)
    balance = await wm.get_balance(pubkey)
    print(f"💰 Баланс гаманця {pubkey}: {balance:.6f} SOL")

    await wm.close()

if __name__ == "__main__":
    asyncio.run(main())
