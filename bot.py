import requests
from bs4 import BeautifulSoup
import os

# --- Nastavení ---
URL = "https://www.reservio.cz/b/psychosomaticka-pece/booking?step=2&serviceId=1f6c9687-412e-4fe1-9413-26fd378af0cc"
CHECK_DATE = "28. 11."
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(telegram_url, data=data)
    except Exception as e:
        print("Chyba při odesílání zprávy:", e)

def check_availability():
    try:
        r = requests.get(URL, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        if CHECK_DATE in soup.text and "obsazeno" not in soup.text.lower():
            return True
    except Exception as e:
        print("Chyba při načítání stránky:", e)
    return False

if __name__ == "__main__":
    if check_availability():
        send_telegram_message(f"🟢 Uvolnil se termín {CHECK_DATE} u Hany Salačové!\n{URL}")
    else:
        print("Zatím nic volného.")
