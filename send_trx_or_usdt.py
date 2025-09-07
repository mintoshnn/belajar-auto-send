import time
from tronpy import Tron
from tronpy.keys import PrivateKey

# Konfigurasi
PRIVATE_KEY = 'YOUR_PRIVATE_KEY_HERE'  # Ganti dengan private key Anda
TO_ADDRESS = 'TARGET_ADDRESS_HERE'     # Ganti dengan alamat tujuan
AMOUNT_USDT = 10                       # Jumlah USDT yang ingin dikirim
INTERVAL_SECONDS = 60                  # Interval pengiriman dalam detik

# Inisialisasi client Tron
client = Tron()

# Load private key
priv_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))

# USDT TRC20 contract address
USDT_CONTRACT = 'TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj'

def send_usdt():
    # Ambil kontrak USDT
    contract = client.get_contract(USDT_CONTRACT)

    # USDT memiliki 6 desimal
    amount_in_sun = int(AMOUNT_USDT * 1_000_000)

    # Buat transaksi transfer USDT
    txn = (
        contract.functions.transfer(TO_ADDRESS, amount_in_sun)
        .with_owner(priv_key.public_key.to_base58check_address())
        .fee_limit(1_000_000)  # fee limit dalam SUN (1 TRX = 1_000_000 SUN)
        .build()
        .sign(priv_key)
    )

    # Kirim transaksi
    result = txn.broadcast().wait()
    print(f"Sent {AMOUNT_USDT} USDT to {TO_ADDRESS}, txid: {result['txid']}")

if __name__ == "__main__":
    while True:
        try:
            send_usdt()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(INTERVAL_SECONDS)
