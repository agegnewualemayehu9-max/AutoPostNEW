import requests
import time
from datetime import datetime
import telebot

# ===== CONFIG =====
BOT_TOKEN = "8362622272:AAG7jysYSHCKqNOqK31MD_ZvirbdQ1cqWMY"
TARGET_CHANNEL = "@CryptoPriceAlertt"  # Using channel username directly
POST_INTERVAL = 300  # 5 minutes

BINANCE_API_KEY = "QAf7wJu4rcns4trs9RlZLUcYksPtznXUbksaRUpjonDxboyRyHfxD8qKCZd9cY1r"

SYMBOLS = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "TON": "TONUSDT"
}

bot = telebot.TeleBot(BOT_TOKEN)

def fetch_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    headers = {"X-MBX-APIKEY": BINANCE_API_KEY}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        price = float(data['lastPrice'])
        change_percent = float(data['priceChangePercent'])
        return price, change_percent
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None, None

def format_price_line(name, price, change):
    price_str = f"{price:,.2f}"
    sign_emoji = "🟢" if change >= 0 else "🔴"
    change_str = f"+{change:.0f}%" if change >= 0 else f"{change:.0f}%"
    return f"•| {name}: {price_str} ({change_str}) {sign_emoji}"

def send_message_safe(message):
    retries = 3
    for _ in range(retries):
        try:
            bot.send_message(TARGET_CHANNEL, message, disable_web_page_preview=True)
            print(f"[{datetime.now()}] Posted successfully.")
            return
        except Exception as e:
            print(f"Error sending message, retrying: {e}")
            time.sleep(5)
    print("Failed to send message after 3 retries.")

def main():
    while True:
        lines = []
        for name, symbol in SYMBOLS.items():
            price, change = fetch_price(symbol)
            if price is None:
                continue
            lines.append(format_price_line(name, price, change))
        if lines:
            now = datetime.now().strftime("%I:%M %p")
            message = "\n".join(lines) + f"\n\n⏳ {now}"
            send_message_safe(message)
        time.sleep(POST_INTERVAL)

if __name__ == "__main__":
    main()