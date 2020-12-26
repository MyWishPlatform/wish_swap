from web3 import Web3, HTTPProvider
from wish_swap.settings import GAS_LIMIT, NETWORKS, BNBCLI_PATH
from subprocess import Popen, PIPE
import json


def eth_like_token_mint(network, address, amount):
    w3 = Web3(HTTPProvider(network['node']))
    tx_params = {
        'nonce': w3.eth.getTransactionCount(network['address'], 'pending'),
        'gasPrice': w3.eth.gasPrice,
        'gas': GAS_LIMIT,
    }
    token = network['token']
    contract = w3.eth.contract(address=token['address'], abi=token['abi'])
    initial_tx = contract.functions.mintToUser(Web3.toChecksumAddress(address), amount).buildTransaction(tx_params)
    signed_tx = w3.eth.account.signTransaction(initial_tx, network['private'])
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_hex = tx_hash.hex()
    return tx_hex


def binance_transfer(network, address, amount):
    command_list = [BNBCLI_PATH, 'send',
                    '--from', network['key'],
                    '--to', address,
                    '--amount', f'{amount}:{network["symbol"]}',
                    '--chain-id', network['chain-id'],
                    '--node', network['node'],
                    '--json']

    process = Popen(command_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(input=(network['key-password'] + '\n').encode())
    is_ok = process.returncode == 0
    if is_ok:
        message = json.loads(stdout.decode())
        data = message['TxHash']
    else:
        data = stderr.decode()
    return is_ok, data
