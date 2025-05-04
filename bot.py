import time, threading, random
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from config import *
from payout import send_jackpot_payout
import database as db

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

round_end = time.time() + DEFAULT_ROUND_DURATION
jackpot_pool = 0
ticket_price = float(db.get_setting("ticket_price", DEFAULT_TICKET_PRICE))

def start(update, context):
    update.message.reply_text("Welcome to XRP Jackpot! Use /buy to participate.")

def buy(update, context):
    msg = (
        f"Ticket: {ticket_price} XRP\n"
        f"Send to: `{XRP_ADDRESS}`\n"
        f"Include your wallet address in the message.\n"
        f"Time left: {int(round_end - time.time())} seconds."
    )
    update.message.reply_text(msg, parse_mode="Markdown")

def jackpot(update, context):
    update.message.reply_text(f"Current Jackpot Pool: {jackpot_pool} XRP")

def time_left(update, context):
    update.message.reply_text(f"Time left: {int(round_end - time.time())} seconds")

def setprice(update, context):
    if update.effective_user.id not in ADMIN_IDS:
        return update.message.reply_text("Unauthorized.")
    global ticket_price
    try:
        ticket_price = float(context.args[0])
        db.set_setting("ticket_price", ticket_price)
        update.message.reply_text(f"Ticket price updated to {ticket_price} XRP.")
    except:
        update.message.reply_text("Usage: /setprice 5")

def setprojectwallet(update, context):
    if update.effective_user.id not in ADMIN_IDS:
        return update.message.reply_text("Unauthorized.")
    try:
        wallet = context.args[0]
        db.set_setting("project_wallet", wallet)
        update.message.reply_text(f"Project wallet updated.")
    except:
        update.message.reply_text("Usage: /setprojectwallet r...")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("buy", buy))
dispatcher.add_handler(CommandHandler("jackpot", jackpot))
dispatcher.add_handler(CommandHandler("time", time_left))
dispatcher.add_handler(CommandHandler("setprice", setprice))
dispatcher.add_handler(CommandHandler("setprojectwallet", setprojectwallet))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Running Jackpot Bot"

def round_loop():
    global jackpot_pool, round_end
    while True:
        if time.time() >= round_end:
            entries = db.get_entries()
            if entries:
                winner = random.choice(entries)
                user_id, winner_wallet = winner
                send_jackpot_payout(winner_wallet, jackpot_pool)
                bot.send_message(chat_id=user_id, text=f"You won {jackpot_pool} XRP!")
            else:
                print("No entries.")
            db.clear_entries()
            jackpot_pool = 0
            round_end = time.time() + DEFAULT_ROUND_DURATION
        time.sleep(5)

threading.Thread(target=round_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(port=5000)
