# examples/wallet_example.py

from solana_sdk.wallet import WalletManager
import asyncio

async def main():
    wm = WalletManager()

    print("Створюємо гаманець...")
    wallet = wm.create_keypair()
    pubkey = wallet['public_key']
    secret = wallet['private_key']
    print("Public key:", pubkey)
    print("Secret key:", secret)

    print("\nПеревіряємо публічний ключ:", wm.validate_pubkey(pubkey))
    print("Перевірка пари ключів:", wm.verify_keypair(secret, pubkey))

    print("\nБаланс до airdrop:", await wm.get_balance(pubkey), "SOL")

    print("\nРобимо airdrop 1 SOL...")
    tx_sig = await wm.request_airdrop(pubkey, sol=1)
    if tx_sig:
        print("Transaction Signature:", tx_sig)
        print("Очікуємо підтвердження транзакції...")
        await wm.client.confirm_transaction(tx_sig)
        await asyncio.sleep(2)
    else:
        print("Airdrop не відбувся. Пропускаємо підтвердження.")

    print("\nБаланс після airdrop:", await wm.get_balance(pubkey), "SOL")

    print("\nПідписуємо повідомлення...")
    message = "SolSpy is async now!"
    signature = wm.sign_message(message, secret)
    print("Підпис:", signature)

    await wm.close()

if __name__ == "__main__":
    asyncio.run(main())
