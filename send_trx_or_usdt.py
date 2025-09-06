import json
from tronpy import Tron
from tronpy.keys import PrivateKey

# Konfigurasi
main_account = "YOUR_MAIN_ACCOUNT_ADDRESS"
private_key = "YOUR_PRIVATE_KEY"  # Harus berupa hex string tanpa '0x'
tron_network = "https://api.trongrid.io"  # Mainnet. Gunakan "https://api.shasta.trongrid.io" untuk testnet

# Fungsi untuk mengirim TRX atau USDT (TRC20)
def send_trx_or_usdt(private_key, amount, recipient_address, contract_address=None):
    client = Tron(network=tron_network)
    priv_key = PrivateKey(bytes.fromhex(private_key))
    
    if contract_address:
        # Kirim USDT (TRC20)
        usdt_contract = client.get_contract(contract_address)
        txn = (
            usdt_contract.functions.transfer(recipient_address, int(amount * 10**6))
            .with_owner(main_account)
            .fee_limit(2_000_000)
            .build()
            .sign(priv_key)
        )
    else:
        # Kirim TRX
        txn = (
            client.trx.transfer(main_account, recipient_address, int(amount * 10**6))
            .build()
            .sign(priv_key)
        )

    result = client.trx.broadcast(txn)
    return result

# Konfigurasi pengiriman
recipient_address = "RECIPIENT_ADDRESS"
amount = 10  # Jumlah TRX atau USDT
usdt_contract_address = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"  # Kontrak USDT di Tron mainnet

# Contoh: Kirim USDT
# result = send_trx_or_usdt(private_key, amount, recipient_address, usdt_contract_address)

# Contoh: Kirim TRX
# result = send_trx_or_usdt(private_key, amount, recipient_address)

# Uncomment sesuai kebutuhan
# print(result)