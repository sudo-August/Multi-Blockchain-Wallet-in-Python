import subprocess
import json
from dotenv import load_dotenv
import os
  
from bit import PrivateKeyTestnet
from bit import wif_to_key
from bit.network import NetworkAPI, satoshi_to_currency

from web3 import Web3
from eth_account import Account 

from constants import ETH, BTC, BTCTEST

load_dotenv()
mnemonic = os.getenv("MNEMONIC")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    if coin == ETH:
        sign = account.signTransaction(raw_tx)
        return w3.eth.sendRawTransaction(sign.rawTransaction)
    elif coin == BTCTEST:
        sign = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)

def create_tx(coin, account, to, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas({
            "from": account.address, 
            "to": to, 
            "value": amount
        })
    
        nonce =  w3.eth.getTransactionCount(sender)+1
        
        return {
            'to': to,
            'from': account.address,
            'value': amount,
            'gas': gasEstimate,
            'gasPrice': Web3.eth.generateGasPrice(),
            'nonce': nonce
        }
    elif coin == BTCTEST:
        return account.prepare_transaction(account.address, [(to, amount, BTC)])

def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account().privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)

def derive_wallets():
    command = './derive -g --mnemonic="' + mnemonic + '" --cols=path,address,privkey,pubkey --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    print(keys)
    return keys 

coins = {
    ETH: derive_wallets(),
    BTCTEST: derive_wallets()
}
