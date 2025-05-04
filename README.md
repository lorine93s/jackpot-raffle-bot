# XRP Jackpot Telegram Bot

A Telegram bot that runs a simple XRP jackpot game.

## Features

- Users buy tickets with XRP
- Admins set ticket price and round duration
- Winner receives 95% of jackpot
- 4% to the project’s wallet
- 1% to the bot creator

## Setup

1. Clone repo
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your config in `config.py`
4. Run bot:
   ```
   python bot.py
   ```

## Telegram Webhook Setup

Set your webhook like this:

```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://yourdomain.com/<YOUR_TOKEN>
```

## License

MIT
