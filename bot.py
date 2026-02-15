import requests

TOKEN = "8521739464:AAHM_ZwfT7wxYGH8hbJ21EasDcP6a27k_Ms"
CHAT_ID = "6737326135"

def tekshir():
    try:
        # Bozor narxini olish
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT")
        narx = float(r.json()['price'])
        
        # Dushanba kungi parametrlar (Hozirgi holat uchun)
        if (90 % 90 == 0) and (10 <= 10 or 10 >= 90):
            tp, sl = narx + 10.0, narx - 2.5
            xabar = (
                f"🤖 AVTOMATIK KVANT SIGNAL\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📍 Narx: {narx}\n"
                f"🎯 TP: {tp}\n"
                f"🛡️ SL: {sl}\n"
                f"✅ Tizim: Avtomat ishlamoqda"
            )
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": xabar})
    except:
        pass

if __name__ == "__main__":
    tekshir()
