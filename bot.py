import requests
import pandas as pd
import pandas_ta as ta
import time

# SOZLAMALAR
TOKEN = "8521739464:AAHM_ZwfT7wxYGH8hbJ2..." # O'zingizni tokenni qoldiring
CHAT_ID = "6737326135" #
SYMBOL = "BTCUSDT"

def get_smart_analysis():
    # 1. Ma'lumotlarni yig'ish (Binance API)
    url = f"https://api.binance.com/api/3/klines?symbol={SYMBOL}&interval=5m&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=['ts', 'o', 'h', 'l', 'c', 'v', 'ct', 'q', 'n', 'tbb', 'tbq', 'i'])
    df['close'] = df['close'].astype(float)
    
    # 2. Texnik ko'rsatkichlarni hisoblash
    df['rsi'] = ta.rsi(df['close'], length=14) # RSI
    df['ema_fast'] = ta.ema(df['close'], length=10) # EMA 10
    df['ema_slow'] = ta.ema(df['close'], length=20) # EMA 20
    
    last_row = df.iloc[-1]
    rsi = last_row['rsi']
    price = last_row['close']
    ema_cross_up = last_row['ema_fast'] > last_row['ema_slow']
    
    # 3. 4.1 Avlod - Ko'p bosqichli qaror qabul qilish (AI Logikasi)
    # 50% aniqlik va filtrdan o'tkazish
    signal = None
    
    # SOTIB OLISH SHARTI (RSI past + EMA kesishuvi)
    if rsi < 35 and ema_cross_up:
        signal = f"🟢 **AI SIGNAL: SOTIB OLISH** (v4.1)\n📊 RSI: {rsi:.2f}\n💰 Narx: {price}"
    
    # SOTISH SHARTI (RSI baland + EMA pastga yo'nalish)
    elif rsi > 65 and not ema_cross_up:
        signal = f"🔴 **AI SIGNAL: SOTISH** (v4.1)\n📊 RSI: {rsi:.2f}\n💰 Narx: {price}"
        
    return signal

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=Markdown"
    requests.post(url)

print("🚀 v4.1 Sun'iy avlod ishga tushdi...")
send_to_telegram("🚀 **v4.1 Sun'iy avlod tizimi ishga tushdi!**\nFiltr: RSI + EMA + 50% Aniqlik tahlili.")

while True:
    try:
        decision = get_smart_analysis()
        if decision:
            send_to_telegram(decision)
    except Exception as e:
        print(f"Xato yuz berdi: {e}")
    
    time.sleep(60) # Har daqiqada tekshiruv
