from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.transaction import send_reliable_submission
from config import CREATOR_WALLET, PROJECT_WALLET, XRP_SECRET, XRP_NODE
import time

client = JsonRpcClient(XRP_NODE)
wallet = Wallet(seed=XRP_SECRET, sequence=0)

def send_payment(destination_address, amount):
    try:
        tx = Payment(
            account=wallet.classic_address,
            destination=destination_address,
            amount=str(int(amount * 1_000_000))
        )
        response = send_reliable_submission(tx, client, wallet)
        print(f"Sent {amount} XRP to {destination_address}")
    except Exception as e:
        print(f"Failed to send XRP: {e}")

def send_jackpot_payout(winner_wallet, total_amount):
    to_winner = round(total_amount * 0.95, 6)
    to_project = round(total_amount * 0.04, 6)
    to_creator = round(total_amount * 0.01, 6)

    send_payment(winner_wallet, to_winner)
    send_payment(PROJECT_WALLET, to_project)
    send_payment(CREATOR_WALLET, to_creator)
