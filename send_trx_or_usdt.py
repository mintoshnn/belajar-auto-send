import time
import schedule
from tronpy import Tron
from tronpy.keys import PrivateKey
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Inisialisasi client Tron
client = Tron()

# Alamat kontrak USDT TRC20 di jaringan TRON mainnet
USDT_CONTRACT = 'TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj'

# Alamat tujuan pengiriman USDT
main_account = 'TKSXDA8HfE9E1y39RczVQ1ZascUEtaSToF'

# Daftar akun yang akan dicek dan dikirim USDT-nya
accounts = {
    'YOUR_ADDRESS_1': 'YOUR_PRIVATE_KEY_1',
    'YOUR_ADDRESS_2': 'YOUR_PRIVATE_KEY_2',
    # Tambah sesuai kebutuhan
}

# Minimal saldo USDT untuk trigger pengiriman (dalam USDT, bukan SUN)
min_withdraw = 1.0

# Interval pengecekan dalam detik
scan_interval = 60

def send_usdt(private_key_str, to_address, amount):
    try:
        priv_key = PrivateKey(bytes.fromhex(private_key_str))
        wallet = client.get_account(priv_key.public_key.to_base58check_address())
        contract = client.get_contract(USDT_CONTRACT)

        # USDT TRC20 punya 6 desimal
        amount_in_token = int(amount * 10**6)

        txn = (
            contract.functions.transfer(to_address, amount_in_token)
            .with_owner(priv_key.public_key.to_base58check_address())
            .fee_limit(10_000_000)  # fee limit 10 TRX
            .build()
            .sign(priv_key)
        )
        result = txn.broadcast().wait()
        if result['result']:
            logging.info(f"Transfer {amount} USDT berhasil dari {wallet['address']} ke {to_address}")
        else:
            logging.error(f"Transfer gagal: {result}")
    except Exception as e:
        logging.error(f"Error saat transfer USDT: {e}")

def check_and_send():
    for address, priv_key in accounts.items():
        try:
            balance = client.get_token_balance(USDT_CONTRACT, address)
            balance_usdt = balance / 10**6  # konversi ke USDT
            logging.info(f"Saldo USDT {address}: {balance_usdt}")
            if balance_usdt >= min_withdraw:
                logging.info(f"Saldo cukup, mengirim {balance_usdt} USDT ke {main_account}")
                send_usdt(priv_key, main_account, balance_usdt)
            else:
                logging.info(f"Saldo kurang dari {min_withdraw} USDT, skip pengiriman.")
        except Exception as e:
            logging.error(f"Error cek saldo {address}: {e}")

logging.info("Memulai auto-send USDT dengan interval {} detik".format(scan_interval))
schedule.every(scan_interval).seconds.do(check_and_send)

while True:
    schedule.run_pending()
    time.sleep(1)
