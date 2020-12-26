from wish_swap.payments.models import Payment
from wish_swap.transfers.models import Transfer
from wish_swap.transfers.api import eth_like_token_mint
from wish_swap.settings import NETWORKS


def save_payment(message):
    blockchain = message['from_blockchain']
    payment = Payment(
        address=message['address'],
        tx_hash=message['tx_hash'],
        currency=NETWORKS[blockchain]['token']['symbol'],
        amount=message['amount'],
    )
    payment.save()
    return payment


def create_transfer(message, payment, amount):
    transfer = Transfer(
        payment=payment,
        address=message['to_address'],
        currency=message['to_currency'],
        amount=amount,
    )
    transfer.save()
    return transfer


def parse_payment_message(message):
    tx_hash = message['transactionHash']
    blockchain = message['from_blockchain']
    currency = NETWORKS[blockchain]['token']['symbol']
    if not Payment.objects.filter(tx_hash=tx_hash, currency=currency).count() > 0:
        payment = save_payment(message)

        # TODO: calculate amount
        amount = None

        transfer = create_transfer(message, payment, amount)

        blockchain = message['to_blockchain']
        if blockchain in ('Ethereum', 'Binance-Smart-Chain'):
            try:
                transfer.tx_hash = eth_like_token_mint(
                    network=NETWORKS[blockchain],
                    address=transfer.address,
                    amount=transfer.amount
                )
                transfer.status = 'TRANSFERRED'
            except Exception as e:
                transfer.tx_error = repr(e)
                transfer.status = 'FAIL'
            transfer.save()
        elif blockchain == 'Binance-Chain':
            pass
        else:
            print('parsing payment: Unknown blockchain', flush=True)
    else:
        print(f'parsing payment:: Tx {tx_hash} already registered', flush=True)
